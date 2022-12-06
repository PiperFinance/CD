from pinatapy import PinataPy
from dotenv import load_dotenv
import os

load_dotenv()

pinata = PinataPy(os.getenv("PINATA_API_KEY", ""),
                  os.getenv("PINATA_API_SECRET", ""))
pinata.
