# import threading
#
# from videoanalytics import VideoHandler
# from fastapi import FastAPI, APIRouter, Header
# from fastapi.responses import StreamingResponse
#
# outputFrame = None
# lock = threading.Lock()
#
# app = FastAPI(title="Test API", openapi_url="/openapi.json")
#
# api_router = APIRouter()
#
#
# @api_router.get("/video")
# async def video_feed(range: str = Header(None)):
#     start, end = range.replace("bytes=", "").split("-")
#     start = int(start)
#     end = int(end) if end else start + 1024 * 1024
#
#     # handler = VideoHandler()
#
#
# app.include_router(api_router)
#

import asyncio
import os

from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack
from aiortc.contrib.media import MediaPlayer, MediaRelay
from av.frame import Frame
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from videoanalytics.analytics import Analyzer

ROOT = os.path.dirname(__file__)
print(ROOT)

app = FastAPI()

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

relay = None
player = None


class Offer(BaseModel):
    sdp: str
    type: str


class VideoTransformTrack(MediaStreamTrack):
    kind = "video"

    def __init__(self, track):
        super().__init__()
        self.track = track
        self._analyzer = Analyzer()

    async def recv(self) -> Frame:
        frame = await self.track.recv()
        self._analyzer.process_frame(frame)
        return frame


def create_local_tracks():
    global relay, player, analyse
    options = {"framerate": "30", "video_size": "640x360"}
    if analyse:
        relay = MediaRelay()
        player = MediaPlayer(ROOT + '/resources/videoplayback.mp4', options=options)
        return None, VideoTransformTrack(relay.subscribe(player.video))
    else:

        if relay is None:
            player = MediaPlayer(ROOT + '/resources/videoplayback.mp4', options=options)
            # if platform.system() == "Darwin":
            #     player = MediaPlayer(
            #         "default:none", format="avfoundation", options=options
            #     )
            # elif platform.system() == "Windows":
            #     player = MediaPlayer(
            #         "video=Integrated Camera", format="dshow", options=options
            #     )
            # else:
            #     player = MediaPlayer("/dev/video0", format="v4l2", options=options)
            relay = MediaRelay()
        return None, relay.subscribe(player.video)


@app.get("/")
async def index():
    return "asdf"


@app.post("/offer")
async def offer(params: Offer):
    offer_data = RTCSessionDescription(sdp=params.sdp, type=params.type)

    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print("Connection state is %s" % pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    # open media source
    audio, video = create_local_tracks()

    if audio:
        _ = pc.addTrack(audio)
    if video:
        _ = pc.addTrack(video)

    await pc.setRemoteDescription(offer_data)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}


pcs = set()


@app.on_event("shutdown")
async def on_shutdown():
    # close peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()


analyse = True

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
