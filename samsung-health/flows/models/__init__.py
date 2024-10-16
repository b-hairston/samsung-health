from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Exercise(BaseModel):
    calories_burned: Optional[int] = Field (None, alias='total_calorie')
    duration: Optional[int] = Field(None, alias='com.samsung.health.exercise.duration')
    start_time: datetime = Field(alias='com.samsung.health.exercise.start_time')
    end_time: datetime = Field(alias='com.samsung.health.exercise.end_time')
    update_time: datetime = Field(alias='com.samsung.health.exercise.update_time')
    create_time: datetime = Field(alias='com.samsung.health.exercise.create_time')
    max_speed: Optional[float] = Field(None, alias='com.samsung.health.exercise.max_speed')
    mean_speed: Optional[float] = Field(None, alias='com.samsung.health.exercise.mean_speed')
    avg_cadence: Optional[float] = Field(None, alias='com.samsung.health.exercise.mean_cadence')
    max_cadence: Optional[float] = Field(None, alias='com.samsung.health.exercise.max_cadence')
    min_heart_rate: Optional[int] = Field(None, alias='com.samsung.health.exercise.min_heart_rate')
    distance: Optional[float] = Field(None, alias='com.samsung.health.exercise.distance')
    vo2_max: Optional[float] = Field(None, alias='com.samsung.health.exercise.vo2_max')
    time_zone: Optional[str] = Field(None, alias='com.samsung.health.exercise.time_offset')
    sweat_loss: Optional[int] = Field(None, alias='com.samsung.health.exercise.sweat_loss')


class Steps(BaseModel):
    step_count: int
    active_time: int
    update_time: datetime
    create_time: datetime
    speed: float
    distance: float
    calorie: float
    walk_step_count: int

class HeartRate(BaseModel):
    start_time: datetime = Field(alias='com.samsung.health.heart_rate.start_time')
    end_time: datetime = Field(alias='com.samsung.health.heart_rate.end_time')
    update_time: datetime = Field(alias='com.samsung.health.heart_rate.update_time')
    create_time: datetime = Field(alias='com.samsung.health.heart_rate.create_time')
    max_heart_rate: Optional[int] = Field(None, alias='com.samsung.health.heart_rate.max')
    min_heart_rate: Optional[int] = Field(None, alias='com.samsung.health.heart_rate.min')
    time_zone: str = Field(alias='com.samsung.health.heart_rate.time_offset')
    heart_rate: int = Field(alias= 'com.samsung.health.heart_rate.heart_rate')

class SkinTemp(BaseModel):
    start_time: datetime
    end_time: datetime
    create_time: datetime
    max_temp: float = Field(alias='max')
    min_temp: float = Field(alias='min')
    temp: float = Field(alias='temperature')
    time_zone: str = Field(alias='time_offset')