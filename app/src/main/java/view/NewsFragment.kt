package view

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.recyclerview.widget.LinearLayoutManager
import com.chaquo.python.Python
import com.example.inprogress.R
import com.google.gson.GsonBuilder
import controller.MainAdapter
import kotlinx.android.synthetic.main.fragment_news.view.*
import java.io.IOException


// TODO: Rename parameter arguments, choose names that match
// the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
private const val ARG_PARAM1 = "param1"
private const val ARG_PARAM2 = "param2"

/**
 * A simple [Fragment] subclass.
 * Use the [NewsFragment.newInstance] factory method to
 * create an instance of this fragment.
 */
class NewsFragment : Fragment() {
    // TODO: Rename and change types of parameters
    private var param1: String? = null
    private var param2: String? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        arguments?.let {
            param1 = it.getString(ARG_PARAM1)
            param2 = it.getString(ARG_PARAM2)
        }


    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        var raw = initNews()
        if (raw == "error") {
            var errorMsg = "Error parsing Thomson Reuters news. Please contact the creator for its resolution."
            Toast.makeText(activity, errorMsg, Toast.LENGTH_LONG).show()
        } else if (raw.contains("Error")) {
            Toast.makeText(activity, raw, Toast.LENGTH_LONG).show()
        } else {
            read_json(raw)
        }
    }


    private fun initNews(): String{
        val python = Python.getInstance()
        val pythonFile = python.getModule("WorldNews_py")
        return pythonFile.callAttr("news").toString()
    }

    fun read_json(raw: String){

        try {

            val gson = GsonBuilder().create()
            val homeFeed = gson.fromJson(raw, HomeFeed::class.java)

            activity?.runOnUiThread {
                view?.worldNews?.adapter = MainAdapter(homeFeed)
            }


        } catch (e: IOException) {

        }
    }


    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_news, container, false)

        view.worldNews.layoutManager = LinearLayoutManager(activity)

        return view
    }


    companion object {
        /**
         * Use this factory method to create a new instance of
         * this fragment using the provided parameters.
         *
         * @param param1 Parameter 1.
         * @param param2 Parameter 2.
         * @return A new instance of fragment NewsFragment.
         */
        // TODO: Rename and change types and number of parameters
        @JvmStatic
        fun newInstance(param1: String, param2: String) =
            NewsFragment().apply {
                arguments = Bundle().apply {
                    putString(ARG_PARAM1, param1)
                    putString(ARG_PARAM2, param2)
                }
            }
    }
}

class HomeFeed(val News: List<News>)

class News(val title: String, val description: String, val time: String, val link: String)