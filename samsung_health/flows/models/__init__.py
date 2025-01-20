from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class Exercise(BaseModel):
    calories_burned: Optional[float] = Field(None, alias='total_calorie')
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
    max_heart_rate: Optional[int] = Field(None, alias='com.samsung.health.exercise.max_heart_rate')
    mean_heart_rate: Optional[float] = Field(None, alias='com.samsung.health.exercise.mean_heart_rate')
    distance: Optional[float] = Field(None, alias='com.samsung.health.exercise.distance')
    vo2_max: Optional[float] = Field(None, alias='com.samsung.health.exercise.vo2_max')
    time_zone: Optional[str] = Field(None, alias='com.samsung.health.exercise.time_offset')
    sweat_loss: Optional[int] = Field(None, alias='com.samsung.health.exercise.sweat_loss')
    altitude_gain: Optional[float] = Field(None, alias='com.samsung.health.exercise.altitude_gain')
    altitude_loss: Optional[float] = Field(None, alias='com.samsung.health.exercise.altitude_loss')
    incline_distance: Optional[float] = Field(None, alias='com.samsung.health.exercise.incline_distance')
    decline_distance: Optional[float] = Field(None, alias='com.samsung.health.exercise.decline_distance')
    max_altitude: Optional[float] = Field(None, alias='com.samsung.health.exercise.max_altitude')
    min_altitude: Optional[float] = Field(None, alias='com.samsung.health.exercise.min_altitude')
    comment: Optional[str] = Field(None, alias='com.samsung.health.exercise.comment')
    device_uuid: Optional[str] = Field(None, alias='com.samsung.health.exercise.deviceuuid')
    live_data: Optional[str] = Field(None, alias='com.samsung.health.exercise.live_data')
    mean_power: Optional[float] = Field(None, alias='com.samsung.health.exercise.mean_power')
    max_power: Optional[float] = Field(None, alias='com.samsung.health.exercise.max_power')
    mean_caloric_burn_rate: Optional[float] = Field(None, alias='com.samsung.health.exercise.mean_caloricburn_rate')
    max_caloric_burn_rate: Optional[float] = Field(None, alias='com.samsung.health.exercise.max_caloricburn_rate')
    mean_rpm: Optional[float] = Field(None, alias='com.samsung.health.exercise.mean_rpm')
    max_rpm: Optional[float] = Field(None, alias='com.samsung.health.exercise.max_rpm')
    exercise_type: Optional[int] = Field(None, alias='com.samsung.health.exercise.exercise_type')
    custom_type: Optional[str] = Field(None, alias='com.samsung.health.exercise.exercise_custom_type')
    custom: Optional[str] = Field(None, alias='com.samsung.health.exercise.custom')
    pkg_name: Optional[str] = Field(None, alias='com.samsung.health.exercise.pkg_name')
    data_uuid: Optional[str] = Field(None, alias='com.samsung.health.exercise.datauuid')
    heart_rate_sample_count: Optional[int] = Field(None, alias='heart_rate_sample_count')
    start_latitude: Optional[float] = Field(None, alias='start_latitude')
    start_longitude: Optional[float] = Field(None, alias='start_longitude')
    title: Optional[str] = Field(None, alias='title')
    tracking_status: Optional[int] = Field(None, alias='tracking_status')
    activity_type: Optional[int] = Field(None, alias='activity_type')
    


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
