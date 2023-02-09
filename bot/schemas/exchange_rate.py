from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, validator


class SchemaBodyCurrency(BaseModel):
    id: str = Field(alias='ID')
    num_code: str = Field(alias='NumCode')
    char_code: str = Field(alias='CharCode')
    nominal: int = Field(alias='Nominal')
    name: str = Field(alias='Name')
    value: float = Field(alias='Value')
    previous: float = Field(alias='Previous')


class SchemaCurrency(BaseModel):
    aud: SchemaBodyCurrency = Field(alias='AUD')
    azn: SchemaBodyCurrency = Field(alias='AZN')
    gbp: SchemaBodyCurrency = Field(alias='GBP')
    amd: SchemaBodyCurrency = Field(alias='AMD')
    byn: SchemaBodyCurrency = Field(alias='BYN')
    bgn: SchemaBodyCurrency = Field(alias='BGN')
    brl: SchemaBodyCurrency = Field(alias='BRL')
    huf: SchemaBodyCurrency = Field(alias='HUF')
    vnd: SchemaBodyCurrency = Field(alias='VND')
    hkd: SchemaBodyCurrency = Field(alias='HKD')
    gel: SchemaBodyCurrency = Field(alias='GEL')
    dkk: SchemaBodyCurrency = Field(alias='DKK')
    aed: SchemaBodyCurrency = Field(alias='AED')
    usd: SchemaBodyCurrency = Field(alias='USD')
    eur: SchemaBodyCurrency = Field(alias='EUR')
    egp: SchemaBodyCurrency = Field(alias='EGP')
    inr: SchemaBodyCurrency = Field(alias='INR')
    idr: SchemaBodyCurrency = Field(alias='IDR')
    kzt: SchemaBodyCurrency = Field(alias='KZT')
    cad: SchemaBodyCurrency = Field(alias='CAD')
    qar: SchemaBodyCurrency = Field(alias='QAR')
    kgs: SchemaBodyCurrency = Field(alias='KGS')
    cny: SchemaBodyCurrency = Field(alias='CNY')
    mdl: SchemaBodyCurrency = Field(alias='MDL')
    nzd: SchemaBodyCurrency = Field(alias='NZD')
    nok: SchemaBodyCurrency = Field(alias='NOK')
    pln: SchemaBodyCurrency = Field(alias='PLN')
    ron: SchemaBodyCurrency = Field(alias='RON')
    xdr: SchemaBodyCurrency = Field(alias='XDR')
    sgd: SchemaBodyCurrency = Field(alias='SGD')
    tjs: SchemaBodyCurrency = Field(alias='TJS')
    thb: SchemaBodyCurrency = Field(alias='THB')
    tmt: SchemaBodyCurrency = Field(alias='TMT')
    uzs: SchemaBodyCurrency = Field(alias='UZS')
    uah: SchemaBodyCurrency = Field(alias='UAH')
    czk: SchemaBodyCurrency = Field(alias='CZK')
    sek: SchemaBodyCurrency = Field(alias='SEK')
    chf: SchemaBodyCurrency = Field(alias='CHF')
    rsd: SchemaBodyCurrency = Field(alias='RSD')
    zar: SchemaBodyCurrency = Field(alias='ZAR')
    krw: SchemaBodyCurrency = Field(alias='KRW')
    jpy: SchemaBodyCurrency = Field(alias='JPY')


class SchemaBodyCurrentExchangeRate(BaseModel):
    date: datetime = Field(alias='Date')
    previous_date: datetime = Field(alias='PreviousDate')
    previous_url: str = Field(alias='PreviousURL')
    timestamp: datetime = Field(alias='Timestamp')
    currency: SchemaCurrency = Field(alias='Valute')


class CurrencyValue(BaseModel):
    value: Decimal = Field()

    @validator('value')
    def quantize(cls, value):
        if value <= 0:
            raise ValueError('The value must be > 0')
        return Decimal(value).quantize(Decimal('1.0000'))
