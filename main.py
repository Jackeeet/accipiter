import asyncio
import os

from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer, MediaRelay
from av import VideoFrame
from av.frame import Frame
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse

from routers import rules
from videoanalytics.analytics import Analyzer

ROOT = os.path.dirname(__file__)

app = FastAPI()

app.include_router(rules.router)


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        content = {"message": "Internal server error", "details": str(e)}
        return JSONResponse(content=content, status_code=500)


app.middleware('http')(catch_exceptions_middleware)

origins = [
    'http://localhost:3000',
    'http://localhost:3000/',
    'localhost:3000',
    'localhost:3000/'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

relay = None
player = None


class Offer(BaseModel):
    sdp: str
    type: str


class VideoTransformTrack(MediaStreamTrack):
    kind = "video"

    def __init__(self, track, analyzer: Analyzer):
        super().__init__()
        self.track = track
        self._analyzer = analyzer

    async def recv(self) -> Frame:
        source_frame = await self.track.recv()
        frame = self._analyzer.process_frame(source_frame.to_ndarray(format="bgr24"))
        new_frame = VideoFrame.from_ndarray(frame, format="bgr24")
        new_frame.pts = source_frame.pts
        new_frame.time_base = source_frame.time_base
        return new_frame


def create_local_tracks(analyzer: Analyzer):
    global relay, player, analyse
    options = {"framerate": "30", "video_size": "640x360"}
    if analyse:
        relay = MediaRelay()
        player = MediaPlayer(ROOT + '/resources/videoplayback.mp4', options=options)
        return None, VideoTransformTrack(relay.subscribe(player.video), analyzer)
    else:
        if relay is None:
            player = MediaPlayer(ROOT + '/resources/videoplayback.mp4', options=options)
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

    # analyzer = Analyzer()

    # open media source
    global analyzer
    audio, video = create_local_tracks(analyzer)

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


# analyse = True
analyse = False

analyzer = Analyzer() if analyse else None

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
