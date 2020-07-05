package controller

import android.content.Intent
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.example.inprogress.R
import com.example.inprogress.ShowLinkActivity
import kotlinx.android.synthetic.main.list_row.view.*
import view.HomeFeed
import view.News


class MainAdapter(val homeFeed: HomeFeed): RecyclerView.Adapter<MainAdapter.ViewHolder>() {

    override fun getItemCount(): Int {

        return homeFeed.News.count()
    }

    override fun onCreateViewHolder(parent: ViewGroup, position: Int): ViewHolder {
        val layoutInflater = LayoutInflater.from(parent?.context)
        val cellForRow = layoutInflater.inflate(R.layout.list_row, parent, false)
        return ViewHolder(cellForRow)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val article = homeFeed.News.get(position)
        holder.view.title.text = article.title.replace("\n", " ")
        holder.view.description.text = article.description.replace("\n", " ").replace("\t", " ")
        holder.view.publication_time.text = article.time.replace("\n", " ")

        holder.newsLink = article

    }

    class ViewHolder(val view: View, var newsLink: News? = null): RecyclerView.ViewHolder(view) {

        companion object {
            val NEWS_LINK_KEY = "NEWS_LINK"
        }

        init {
            view.link_btn.setOnClickListener {
                var intent = Intent(view.context, ShowLinkActivity::class.java)
                intent.putExtra(NEWS_LINK_KEY, newsLink?.link)
                view.context.startActivity(intent)
            }
        }

    }

}

