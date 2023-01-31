import asyncio
import os
import sys

from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer, MediaRelay
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from routers import detectors, rules
from videoanalytics import VideoHandler
from videoanalytics.analytics import Analyzer
from videoanalytics.video.models.offer import Offer
from videoanalytics.video.videoTransformTrack import VideoTransformTrack

pcs = set()
relay = MediaRelay()
# analyze = True
analyze = False
# analyzer = Analyzer()
ROOT = os.path.dirname(__file__)

app = FastAPI()
app.include_router(rules.router)
app.include_router(detectors.router)


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
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/offer")
async def offer(params: Offer):
    offer_data = RTCSessionDescription(sdp=params.sdp, type=params.type)

    pc = RTCPeerConnection()
    pcs.add(pc)
    await pc.setRemoteDescription(offer_data)

    options = {"framerate": "30", "video_size": "640x360"}
    player = MediaPlayer(ROOT + '/resources/videoplayback.mp4', options=options, loop=True)
    track = VideoTransformTrack(relay.subscribe(player.video), analyzer) if analyze else relay.subscribe(player.video)
    pc.addTrack(track)

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print("Connection state is %s" % pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}


@app.on_event("shutdown")
async def on_shutdown():
    coroutines = [pc.close() for pc in pcs]  # close peer connections
    await asyncio.gather(*coroutines)
    pcs.clear()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        import uvicorn

        uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
    else:
        videoHandler = VideoHandler()
        videoHandler.run()
