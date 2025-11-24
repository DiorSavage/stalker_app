from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from presentation.api.v1.controllers.user_controller import router as UserRouter
from presentation.api.v1.controllers.post_controller import router as PostRouter

def create_app():
	app = FastAPI(
		description="ddd stalk app",
		docs_url="/api/docs",
		title="DDD Stalker App",
		debug=True
	)
	app.include_router(UserRouter)
	app.include_router(PostRouter)

	@app.get("/", response_class=RedirectResponse, include_in_schema=False)
	def redirect_to_docs():
		return "/api/docs"
	
	return app