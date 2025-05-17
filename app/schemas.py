from pydantic import BaseModel, Field, validator, ValidationError
from typing import Optional, List, TypeVar, Generic

class EventOut(BaseModel):
    eventid: int
    iyear: Optional[int] = None
    imonth: Optional[int] = None
    iday: Optional[int] = None
    location: Optional[str] = None
    summary: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    crit1: Optional[int] = None
    crit2: Optional[int] = None
    crit3: Optional[int] = None
    addnotes: Optional[str] = None
    scite1: Optional[str] = None
    scite2: Optional[str] = None
    scite3: Optional[str] = None
    dbsource: Optional[str] = None
    targetid: Optional[int] = None
    gid: Optional[int] = None
    weaponid: Optional[int] = None
    attackid: Optional[int] = None
    nkill: Optional[int] = None
    nkillus: Optional[int] = None
    nkillter: Optional[int] = None
    nwound: Optional[int] = None
    nwoundte: Optional[int] = None
    property: Optional[int] = None
    propextent: Optional[int] = None
    propextent_txt: Optional[str] = None
    propvalue: Optional[int] = None
    propcomment: Optional[str] = None
    ishostkid: Optional[int] = None
    nhostkid: Optional[int] = None
    nhostkidus: Optional[int] = None
    nhours: Optional[int] = None
    ndays: Optional[int] = None
    divert: Optional[str] = None
    kidihijcountry: Optional[str] = None
    ransom: Optional[int] = None
    ransomamt: Optional[int] = None
    ransomamtus: Optional[str] = None
    ransompaid: Optional[int] = None
    ransompaidus: Optional[str] = None
    ransomnote: Optional[str] = None
    hostkidoutcome: Optional[int] = None
    hostkidoutcome_txt: Optional[str] = None
    nreleased: Optional[int] = None
    regionid: Optional[int] = None
    countryid: Optional[int] = None

    class Config:
        from_attributes = True

class GroupOut(BaseModel):
    gid: int
    gname: Optional[str] = None
    gsubname: Optional[str] = None
    gname2: Optional[str] = None
    gsubname2: Optional[str] = None
    gname3: Optional[str] = None
    gsubname3: Optional[str] = None
    motive: Optional[str] = None
    guncertain1: Optional[int] = None
    guncertain2: Optional[int] = None
    guncertain3: Optional[int] = None
    individual: Optional[int] = None
    nperps: Optional[int] = None
    nperpcap: Optional[int] = None
    claimed: Optional[int] = None
    claimmode: Optional[int] = None
    claimmode_txt: Optional[str] = None
    claim2: Optional[int] = None
    claimmode2: Optional[int] = None
    claimmode2_txt: Optional[str] = None
    claim3: Optional[int] = None
    claimmode3: Optional[int] = None
    claimmode3_txt: Optional[str] = None
    compclaim: Optional[str] = None

    class Config:
        from_attributes = True

class WeaponOut(BaseModel):
    weaponid: int
    weaptype1: Optional[int] = None
    weaptype1_txt: Optional[str] = None
    weapsubtype1: Optional[int] = None
    weapsubtype1_txt: Optional[str] = None
    weaptype2: Optional[int] = None
    weaptype2_txt: Optional[str] = None
    weapsubtype2: Optional[int] = None
    weapsubtype2_txt: Optional[str] = None
    weaptype3: Optional[int] = None
    weaptype3_txt: Optional[str] = None
    weapsubtype3: Optional[int] = None
    weapsubtype3_txt: Optional[str] = None
    weaptype4: Optional[int] = None
    weaptype4_txt: Optional[str] = None
    weapsubtype4: Optional[int] = None
    weapsubtype4_txt: Optional[str] = None
    weapdetail: Optional[str] = None

    class Config:
        from_attributes = True

class TargetOut(BaseModel):
    targetid: int
    targtype1: Optional[int] = None
    targtype1_txt: Optional[str] = None
    targsubtype1: Optional[int] = None
    targsubtype1_txt: Optional[str] = None
    corp1: Optional[str] = None
    target1: Optional[str] = None
    natlty1: Optional[int] = None
    natlty1_txt: Optional[str] = None
    targtype2: Optional[int] = None
    targtype2_txt: Optional[str] = None
    targsubtype2: Optional[int] = None
    targsubtype2_txt: Optional[str] = None
    corp2: Optional[str] = None
    target2: Optional[str] = None
    natlty2: Optional[int] = None
    natlty2_txt: Optional[str] = None
    targtype3: Optional[int] = None
    targtype3_txt: Optional[str] = None
    targsubtype3: Optional[int] = None
    targsubtype3_txt: Optional[str] = None
    corp3: Optional[str] = None
    target3: Optional[str] = None
    natlty3: Optional[int] = None
    natlty3_txt: Optional[str] = None
    countryid: Optional[int] = None
    regionid: Optional[int] = None

    class Config:
        from_attributes = True

class RegionOut(BaseModel):
    regionid: int
    region: str

    class Config:
        from_attributes = True

class CountryOut(BaseModel):
    countryid: int
    countrycode: Optional[int] = None
    country: str
    provstate: Optional[str] = None
    city: Optional[str] = None
    regionid: Optional[int] = None

    class Config:
        from_attributes = True

class AttackOut(BaseModel):
    attackid: int
    attacktype: Optional[str] = None

    class Config:
        from_attributes = True

DataType = TypeVar('DataType') # Mendefinisikan tipe generik
class PaginatedResponse(BaseModel, Generic[DataType]):
    status: str = "success"
    message: Optional[str] = None
    page: Optional[int] = None
    total_pages: Optional[int] = None
    total_items: Optional[int] = None # Tambahan: jumlah total item
    data: List[DataType]

    class Config:
        from_attributes = True

class EventQueryParams(BaseModel):
    page: int = Field(1, ge=1, description="Nomor halaman", error={"ge": "Nomor halaman harus lebih besar atau sama dengan 1"})
    limit: int = Field(10, ge=1, le=100, description="Jumlah item per halaman", error={"ge": "Jumlah item per halaman harus lebih besar atau sama dengan 1", "le": "Jumlah item per halaman harus kurang dari atau sama dengan 100"})
    iyear: Optional[int] = Field(None, ge=1970, description="Filter berdasarkan Tahun", error={"ge": "Tahun harus lebih besar atau sama dengan 1970"})
    imonth: Optional[int] = Field(None, ge=1, le=12, description="Filter berdasarkan Bulan", error={"ge": "Bulan harus lebih besar atau sama dengan 1", "le": "Bulan harus kurang dari atau sama dengan 12"})
    iday: Optional[int] = Field(None, ge=1, le=31, description="Filter berdasarkan Hari", error={"ge": "Hari harus lebih besar atau sama dengan 1", "le": "Hari harus kurang dari atau sama dengan 31"})
    location: Optional[str] = Field(None, description="Filter berdasarkan Lokasi")
    crit1: Optional[int] = Field(None, ge=0, le=1, description="Filter berdasarkan Kriteria 1", error={"ge": "Kriteria 1 harus lebih besar atau sama dengan 0", "le": "Kriteria 1 harus kurang dari atau sama dengan 1"})
    crit2: Optional[int] = Field(None, ge=0, le=1, description="Filter berdasarkan Kriteria 2", error={"ge": "Kriteria 2 harus lebih besar atau sama dengan 0", "le": "Kriteria 2 harus kurang dari atau sama dengan 1"})
    crit3: Optional[int] = Field(None, ge=0, le=1, description="Filter berdasarkan Kriteria 3", error={"ge": "Kriteria 3 harus lebih besar atau sama dengan 0", "le": "Kriteria 3 harus kurang dari atau sama dengan 1"})
    targetid: Optional[int] = Field(None, ge=1, description="Filter berdasarkan ID Target", error={"ge": "ID Target harus lebih besar atau sama dengan 1"})
    gid: Optional[int] = Field(None, ge=1, description="Filter berdasarkan ID Grup", error={"ge": "ID Grup harus lebih besar atau sama dengan 1"})
    weaponid: Optional[int] = Field(None, ge=1, description="Filter berdasarkan ID Senjata", error={"ge": "ID Senjata harus lebih besar atau sama dengan 1"})
    attackid: Optional[int] = Field(None, ge=1, description="Filter berdasarkan ID Serangan", error={"ge": "ID Serangan harus lebih besar atau sama dengan 1"})
    regionid: Optional[int] = Field(None, ge=1, description="Filter berdasarkan ID Wilayah", error={"ge": "ID Wilayah harus lebih besar atau sama dengan 1"})
    region_name: Optional[str] = Field(None, description="Filter berdasarkan Nama Wilayah")
    countryid: Optional[int] = Field(None, ge=1, description="Filter berdasarkan ID Negara", error={"ge": "ID Negara harus lebih besar atau sama dengan 1"})
    group_name: Optional[str] = Field(None, description="Filter berdasarkan Nama Grup")
    weapon_type: Optional[str] = Field(None, description="Filter berdasarkan Tipe Senjata")
    target_name: Optional[str] = Field(None, description="Filter berdasarkan Nama Target")
    country_name: Optional[str] = Field(None, description="Filter berdasarkan Nama Negara")
    attacktype: Optional[str] = Field(None, description="Filter berdasarkan Tipe Serangan")
    sort_by: str = Field("eventid", description="Urutkan berdasarkan field")
    order: str = Field("asc", description="Urutan (asc/desc)")
    
@validator("order")
def validate_order(cls, value):
    if isinstance(value, str):
        return value.lower()
    return value

@validator("order")
def check_order(cls, value):
    if value.lower() not in ["asc", "desc"]:
        raise ValueError([
            {
                "loc": ["query", "order"],
                "msg": "Urutan harus 'asc' atau 'desc'",
                "type": "value_error.any_of",
                "ctx": {"expected": ["asc", "desc"]},
            }
        ])
    return value.lower()

@validator("sort_by")
def validate_sort_by(cls, value):
    allowed_sort_fields = {
        "eventid", "iyear", "imonth", "iday", "location", "crit1", "crit2", "crit3",
        "targetid", "gid", "weaponid", "attackid", "regionid", "countryid"
    }
    if value not in allowed_sort_fields:
        raise ValueError([
            {
                "loc": ["query", "sort_by"],
                "msg": f"Urutkan berdasarkan harus salah satu dari: {', '.join(allowed_sort_fields)}",
                "type": "value_error.any_of",
                "ctx": {"expected": list(allowed_sort_fields)},
            }
        ])
    return value

class EventPathParams(BaseModel):
    event_id: int = Field(..., ge=1, description="ID Event")