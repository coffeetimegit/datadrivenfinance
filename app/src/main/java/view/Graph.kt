package view

import android.graphics.BitmapFactory
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import com.example.inprogress.R
import kotlinx.android.synthetic.main.activity_graph.*

class Graph : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_graph)

        var data = intent.extras
        var graphData = data!!.get("res").toString()

        graph.setImageBitmap(BitmapFactory.decodeFile(graphData))
    }
}