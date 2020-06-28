package com.example.inprogress

import android.graphics.Color
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import com.android.volley.RequestQueue
import com.android.volley.toolbox.JsonArrayRequest
import controller.SupplementalAdapter
import kotlinx.android.synthetic.main.activity_main.*
import android.util.Log
import android.widget.Toast
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.VolleyError
import com.android.volley.toolbox.Volley
import org.json.JSONArray
import org.json.JSONException


var isins = mutableSetOf<String>()
var bondDetails = HashMap<String, List<String>>()
val errorMsg = "Error: Internet connection failure. Cannot render JGB ISINs from Heroku."

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        viewPager.adapter = SupplementalAdapter(supportFragmentManager)
        tabLayoutId.setupWithViewPager(viewPager)

        tabLayoutId.setTabTextColors(Color.GRAY, Color.parseColor("black"))


        var volleyRequest: RequestQueue? = null

        val url = "https://datadrivenfinance.herokuapp.com/"

        isins.add("Select JGB")
        fun getJsonArray(Url: String) {
            val jsonArray = JsonArrayRequest(Request.Method.GET, Url,
                Response.Listener {
                        response: JSONArray ->
                    try {
                        Log.d("Response =====>>> ", response.toString())
                        for (i in 0..response.length() - 1) {
                            val JGB = response.getJSONObject(i)
                            var jgbisin = JGB.getString("ISIN")
                            var jgbcpn = JGB.getString("CPN")
                            var jgbmat = JGB.getString("MAT")
                            val list = listOf(jgbcpn, jgbmat)
                            isins.add(jgbisin)
                            bondDetails.put(jgbisin, list)
                        }

                    } catch (e: JSONException) {
                        Toast.makeText(this, errorMsg, Toast.LENGTH_LONG).show()
                        e.printStackTrace()
                    }
                },
                Response.ErrorListener {
                        error: VolleyError? ->
                    try {
                        Toast.makeText(this, errorMsg, Toast.LENGTH_LONG).show()
                        Log.d("Error: ", error.toString())
                    } catch (e: JSONException) {
                        Toast.makeText(this, errorMsg, Toast.LENGTH_LONG).show()
                        e.printStackTrace()
                    }
                })

            volleyRequest!!.add(jsonArray)
        }

        volleyRequest = Volley.newRequestQueue(this)

        getJsonArray(url)

    }

}

