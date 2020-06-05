package view

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import com.example.inprogress.R
import kotlinx.android.synthetic.main.activity_valuationsres.*

class ValuationsRes : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_valuationsres)

        var data = intent.extras

        if (data != null) {
            valuationOutput.text = data.get("res").toString()
        }

    }
}