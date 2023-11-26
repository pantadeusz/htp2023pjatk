// ApiService.kt
package com.deitel.hackthecliment_mobile

import retrofit2.Call
import retrofit2.http.GET

interface ApiService {
    @GET("/128.0.0.1:8000/farm  ")
    fun getSensorData(): Call<SensorData>
}