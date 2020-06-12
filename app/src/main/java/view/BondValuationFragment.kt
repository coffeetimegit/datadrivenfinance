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
import kotlinx.android.synthetic.main.fragment_bondvaluation.*


// TODO: Rename parameter arguments, choose names that match
// the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
private const val ARG_PARAM1 = "param1"
private const val ARG_PARAM2 = "param2"

/**
 * A simple [Fragment] subclass.
 * Use the [BondValuationFragment.newInstance] factory method to
 * create an instance of this fragment.
 */
class BondValuationFragment : Fragment() {
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

        option = view!!.findViewById(R.id.selectBond)
        result = view!!.findViewById(R.id.bondRes)

        var isins = mutableSetOf<String>()

        if (isins.isEmpty()) {
            val bondList = initBondList()
            val bondSelect = bondList?.get(0).toString()

            var product = ""
            isins.add("Select JGB")
            for (bond in bondSelect) {
                if (bond.toString() != "[" && bond.toString() != "]") {
                    if (bond.toString() == " ") {
                        isins.add(product)
                        product = ""
                    }
                    if (bond.toString() != "'" && bond.toString() != "," && bond.toString() != " ") {
                        product += bond
                    }
                }
            }
            isins.add(product)

            val bondDetails = bondList?.get(1)?.toString()


        option.adapter = ArrayAdapter(activity!!.applicationContext, android.R.layout.simple_list_item_1, isins.toList())

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
                result.text = isins.toList().get(position)
            }
        }


            bondBtn.setOnClickListener {

                if (!bondRes.text.contains("Simple Moving Average")) {

                    if (bondRes.text == "Select JGB" || bondRes.text == "") {
                        Toast.makeText(activity, "Error: Select a JGB from the dropdown!", Toast.LENGTH_SHORT).show()
                    } else {

                        var bondCache = initFIV(bondDetails)

                        var bondCacheImg = bondCache?.get(0).toString()
                        var bondCacheTxt = bondCache?.get(1).toString()

                        if (bondCacheImg != "error") {
                            bondRes.text = bondCacheTxt

                            val intent = Intent(view.context, Graph::class.java)
                            intent.putExtra("res", bondCacheImg)
                            startActivity(intent)
                        }

                        if (bondCacheImg == "error") {
                            Toast.makeText(activity, bondCacheTxt, Toast.LENGTH_LONG).show()
                        }
                    }
                }
            }
        }

        bondClear.setOnClickListener {
            bondRes.text = ""
        }
    }

    private fun initFIV(bondDetails: String?): MutableList<PyObject>? {
        val python = Python.getInstance()
        val pythonFile = python.getModule("BondValuation_py")
        return pythonFile.callAttr("FIV", bondRes.text, bondDetails).asList()
    }

    private fun initBondList(): MutableList<PyObject>? {
        val python = Python.getInstance()
        val pythonFile = python.getModule("BondValuation_py")
        return pythonFile.callAttr("JGBISIN").asList()
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_bondvaluation, container, false)
    }

    companion object {
        /**
         * Use this factory method to create a new instance of
         * this fragment using the provided parameters.
         *
         * @param param1 Parameter 1.
         * @param param2 Parameter 2.
         * @return A new instance of fragment BondValuationFragment.
         */
        // TODO: Rename and change types and number of parameters
        @JvmStatic
        fun newInstance(param1: String, param2: String) =
            BondValuationFragment().apply {
                arguments = Bundle().apply {
                    putString(ARG_PARAM1, param1)
                    putString(ARG_PARAM2, param2)
                }
            }
    }
}