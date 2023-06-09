from pydantic import BaseModel


class SetDataFromCSVRequest(BaseModel):
    full_path: str = "path_to_file"
    sep: str = ";"
    decimal: str = ","
    encoding: str = "utf-8"
