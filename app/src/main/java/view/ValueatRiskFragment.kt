package view

import android.content.Intent
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.*
import com.chaquo.python.PyObject
import com.chaquo.python.Python
import com.example.inprogress.R
import kotlinx.android.synthetic.main.fragment_valueatrisk.*

// TODO: Rename parameter arguments, choose names that match
// the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
private const val ARG_PARAM1 = "param1"
private const val ARG_PARAM2 = "param2"

/**
 * A simple [Fragment] subclass.
 * Use the [ValueatRiskFragment.newInstance] factory method to
 * create an instance of this fragment.
 */
class ValueatRiskFragment : Fragment() {
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

        lateinit var option: Spinner
        lateinit var result: TextView

        option = view!!.findViewById(R.id.selectStockVar)
        result = view!!.findViewById(R.id.varRes)

        val options = getResources().getStringArray(R.array.SP500List)

        option.adapter = ArrayAdapter<String>(activity!!.applicationContext, android.R.layout.simple_list_item_1, options)

        option.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onNothingSelected(parent: AdapterView<*>?) {
                return null!!
            }

            override fun onItemSelected(
                parent: AdapterView<*>?,
                view: View?,
                position: Int,
                id: Long
            ) {
                result.text = options.get(position)
            }

        }

        varBtn.setOnClickListener {
            if (!varRes.text.contains("simulations generated")) {

                if (varRes.text == "Select Stock" || varRes.text == "") {
                    Toast.makeText(activity, "Error: Select a stock from the dropdown!", Toast.LENGTH_SHORT).show()
                } else {

                    var varCache = initVAR()

                    var varCacheImg = varCache?.get(0).toString()
                    var varCacheTxt = varCache?.get(1).toString()

                    if (varCacheImg != "error") {
                        varRes.text = varCacheTxt

                        val intent = Intent(view.context, Graph::class.java)
                        intent.putExtra("res", varCacheImg)
                        startActivity(intent)
                    }

                    if (varCacheImg == "error") {
                        Toast.makeText(activity, varCacheTxt, Toast.LENGTH_LONG).show()
                    }
                }
            }
        }

        varClear.setOnClickListener {
            varRes.text = ""
        }

    }

    private fun initVAR(): MutableList<PyObject>? {
        val python = Python.getInstance()
        val pythonFile = python.getModule("ValueatRisk_py")
        return pythonFile.callAttr("VAR", varRes.text.toString()).asList()
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_valueatrisk, container, false)
    }

    companion object {
        /**
         * Use this factory method to create a new instance of
         * this fragment using the provided parameters.
         *
         * @param param1 Parameter 1.
         * @param param2 Parameter 2.
         * @return A new instance of fragment ValueatRiskFragment.
         */
        // TODO: Rename and change types and number of parameters
        @JvmStatic
        fun newInstance(param1: String, param2: String) =
            ValueatRiskFragment().apply {
                arguments = Bundle().apply {
                    putString(ARG_PARAM1, param1)
                    putString(ARG_PARAM2, param2)
                }
            }
    }
}