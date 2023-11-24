import asyncio
import json
import os
from queue import Queue

from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer, MediaRelay
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from dependencies import video_source
from logmanager.logmanager import LogManager
from routers import detectors, rules, editor, logs, video, settings
from videoanalytics.analytics import Analyzer
from videoanalytics.video.models.offer import Offer
from videoanalytics.video.videoTransformTrack import VideoTransformTrack

pcs = set()
relay = MediaRelay()
logger = LogManager()
analyzer = Analyzer()
analyzer.logger = logger
ROOT = os.path.dirname(__file__)

app = FastAPI()
app.include_router(detectors.router)
app.include_router(editor.router)
app.include_router(rules.router)
app.include_router(video.router)
app.include_router(logs.router)
app.include_router(settings.router)


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.log_error(str(e))
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


@app.get("/analyzer")
async def switch_analyzer(active: bool):
    analyzer.active = active
    if not active:
        analyzer.object_pool = dict()
        analyzer.alerts_queue = Queue()


@app.post("/offer")
async def offer(params: Offer, source: str = Depends(video_source)):
    offer_data = RTCSessionDescription(sdp=params.sdp, type=params.type)

    pc = RTCPeerConnection()
    pcs.add(pc)
    await pc.setRemoteDescription(offer_data)

    options = {"framerate": "30", "video_size": "640x360"}
    player = MediaPlayer(ROOT + "/" + source, options=options, loop=True)
    track = VideoTransformTrack(relay.subscribe(player.video), analyzer)
    pc.addTrack(track)

    @pc.on("datachannel")
    def on_datachannel(channel):
        def received_alerts_request(message):
            return isinstance(message, str) and message == "alerts"

        def received_fps_request(message):
            return isinstance(message, str) and message == "fps"

        def received_objects_request(message):
            return isinstance(message, str) and message == "objects"

        def alert_available():
            return analyzer.active and not analyzer.alerts_queue.empty()

        @channel.on("message")
        def on_message(message):
            if received_alerts_request(message) and alert_available():
                channel.send(analyzer.alerts_queue.get())
            elif received_fps_request(message):
                fps = track.fps
                channel.send(json.dumps({"fps": fps}))
            elif received_objects_request(message):
                obj_count = len(analyzer.object_pool)
                channel.send(json.dumps({"objectCount": obj_count}))

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
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
