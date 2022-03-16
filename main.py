from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from routers import contact

import config

app = FastAPI()

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=config.settings.allowed_host_sources
)

app.include_router(contact.router)


@app.get("/", tags=["Hello World"])
async def root():
    return {
        "message": "Hi! I'm a static website assistant! "
                   "Wanna see everything I can do? Check github.com/svandegar/static-assistant"}

