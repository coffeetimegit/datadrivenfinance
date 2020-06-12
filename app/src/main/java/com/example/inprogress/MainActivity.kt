package com.example.inprogress

import android.graphics.Color
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import controller.SupplementalAdapter
import kotlinx.android.synthetic.main.activity_main.*

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        viewPager.adapter = SupplementalAdapter(supportFragmentManager)
        tabLayoutId.setupWithViewPager(viewPager)

        tabLayoutId.setTabTextColors(Color.GRAY, Color.parseColor("black"))
    }

}