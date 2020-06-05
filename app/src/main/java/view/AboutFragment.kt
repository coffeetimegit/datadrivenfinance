package view

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.Toast
import com.example.inprogress.R

// TODO: Rename parameter arguments, choose names that match
// the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
private const val ARG_PARAM1 = "param1"
private const val ARG_PARAM2 = "param2"

/**
 * A simple [Fragment] subclass.
 * Use the [AboutFragment.newInstance] factory method to
 * create an instance of this fragment.
 */
class AboutFragment : Fragment() {
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
        val kotlin = view.findViewById(R.id.kotlinLogo) as ImageView
        kotlin.setOnClickListener {
            Toast.makeText(activity, "Kotlin: A statically typed programming language that is used for the application's frontend.", Toast.LENGTH_LONG).show()
        }
        val python = view.findViewById(R.id.pythonLogo) as ImageView
        python.setOnClickListener {
            Toast.makeText(activity, "Python: A dynamically typed programming language that is used for the application's backend.", Toast.LENGTH_LONG).show()
        }
        val chaquopy = view.findViewById(R.id.chaquopyLogo) as ImageView
        chaquopy.setOnClickListener {
            Toast.makeText(activity, "Chaquopy: An Application Binary Interface (ABI) that intermixes Kotlin and Java with Python.", Toast.LENGTH_LONG).show()
        }
        val anaconda = view.findViewById(R.id.anacondaLogo) as ImageView
        anaconda.setOnClickListener {
            Toast.makeText(activity, "Anaconda: An open-source distribution of the Python and R programming languages for scientific computing.", Toast.LENGTH_LONG).show()
        }
        val quandl = view.findViewById(R.id.quandlLogo) as ImageView
        quandl.setOnClickListener {
            Toast.makeText(activity, "Quandl: An Application Programming Interface (API) that provides financial, economic and alternative data.", Toast.LENGTH_LONG).show()
        }
        val androidstudio = view.findViewById(R.id.androidStudioLogo) as ImageView
        androidstudio.setOnClickListener {
            Toast.makeText(activity, "Android Studio: The official Integrated Development Environment (IDE) for Google's Android operating system, built on JetBrains' IntelliJ IDEA software and designed specifically for Android development.", Toast.LENGTH_LONG).show()
        }

    }
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_about, container, false)
    }


    companion object {
        /**
         * Use this factory method to create a new instance of
         * this fragment using the provided parameters.
         *
         * @param param1 Parameter 1.
         * @param param2 Parameter 2.
         * @return A new instance of fragment AboutFragment.
         */
        // TODO: Rename and change types and number of parameters
        @JvmStatic
        fun newInstance(param1: String, param2: String) =
            AboutFragment().apply {
                arguments = Bundle().apply {
                    putString(ARG_PARAM1, param1)
                    putString(ARG_PARAM2, param2)
                }
            }
    }
        
}

