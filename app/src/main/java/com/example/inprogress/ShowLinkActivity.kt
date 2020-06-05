package com.example.inprogress

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import controller.MainAdapter
import kotlinx.android.synthetic.main.activity_showlink.*

class ShowLinkActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_showlink)

        val news_link = intent.getStringExtra(MainAdapter.ViewHolder.NEWS_LINK_KEY)

        webViewId.settings.javaScriptEnabled = true
        webViewId.settings.loadWithOverviewMode = true
        webViewId.settings.useWideViewPort = true

        webViewId.loadUrl(news_link.toString())
    }
}