from quart import Quart, request
import aiopg
from quart_jwt_extended import JWTManager
from quart_cors import cors

from datetime import timedelta
from utils.constants import DATABASE_CONFIG
from utils.constants import JWT_KEY
from routers.account import tokenVerification
from routers.account import login
from routers.machines import machines

app = Quart(__name__)
app = cors(app, allow_origin="*" )
app.before_request(tokenVerification)

 
@app.before_serving
async def create_db_pool():
    app.config["pool"] = await  aiopg.create_pool(**DATABASE_CONFIG)


app.register_blueprint(login,context={"pool": create_db_pool}, url_prefix='/account')
app.register_blueprint(machines,context={"pool": create_db_pool}, url_prefix='/machines')
 


app.config["JWT_SECRET_KEY"] = JWT_KEY
jwt = JWTManager(app)


if __name__ == "__main__":
    app.run(debug=True)