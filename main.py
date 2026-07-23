import asyncio

from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli,AgentSession
from livekit.plugins import silero, deepgram, cartesia, groq

from api import RestaurantAgent

load_dotenv()

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    session = AgentSession(
        vad=silero.VAD.load(),
        stt=deepgram.STT(model="nova-2"),
        llm=groq.LLM(model="llama-3.3-70b-versatile"),
        tts=cartesia.TTS(model="sonic-3"),
    )

    await session.start(agent=RestaurantAgent(), room=ctx.room)

    await asyncio.sleep(1)
    await session.say(
        "Hey, welcome to Hardees! What can I get started for you today?",
        allow_interruptions=True,
    )


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))