import android.os.AsyncTask
import android.os.Bundle
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.*


import com.deitel.hackthecliment_mobile.R

class MainActivity : AppCompatActivity() {

    private val BASE_URL = "http://127.0.0.1:8000"
    private val pollingInterval = 2000L // 2 seconds

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val timer = Timer()
        timer.scheduleAtFixedRate(object : TimerTask() {
            override fun run() {
                // Make an API call
                GetSensorDataTask().execute()
            }
        }, 0, pollingInterval)
    }

    inner class GetSensorDataTask : AsyncTask<Void, Void, SensorData>() {
        override fun doInBackground(vararg params: Void?): SensorData? {
            // Retrofit setup
            val retrofit = Retrofit.Builder()
                .baseUrl(BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .build()

            val apiService = retrofit.create(ApiService::class.java)
            val call = apiService.getSensorData()

            try {
                val response = call.execute()
                if (response.isSuccessful) {
                    return response.body()
                }
            } catch (e: Exception) {
                Log.e("API Error", e.toString())
            }

            return null
        }

        override fun onPostExecute(result: SensorData?) {
            // Update UI or trigger alert based on the result
            result?.let {
                if (it.alert) {
                    // Trigger alert
                    showAlert("Alert: Water Quality Issue!")
                } else {
                    // Indicate that water is clean
                    showAlert("Water is clean.")
                }
            }
        }
    }

    private fun showAlert(message: String) {
        // Implement your alert mechanism here
        Log.d("Alert", message)
    }
}