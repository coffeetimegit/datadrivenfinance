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
import kotlinx.android.synthetic.main.fragment_portfoliomgmt.*

// TODO: Rename parameter arguments, choose names that match
// the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
private const val ARG_PARAM1 = "param1"
private const val ARG_PARAM2 = "param2"

/**
 * A simple [Fragment] subclass.
 * Use the [PortfolioMgmtFragment.newInstance] factory method to
 * create an instance of this fragment.
 */
class PortfolioMgmtFragment : Fragment() {
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

    var portfolio = mutableSetOf<String>()
    var portfolioSimulation = mutableListOf<String>()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        lateinit var option: Spinner
        lateinit var result: TextView

        option = view.findViewById(R.id.selectStockMpt)
        result = view.findViewById(R.id.mptRes)

        val options = resources.getStringArray(R.array.SP500List)

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
                portfolio.add(options.get(position))
                if (portfolio.size > 1 && portfolio.contains("Select Stock")) {
                    portfolio.remove("Select Stock")
                }
                result.text = portfolio.toString()
            }

        }

        lateinit var option1: Spinner

        option1 = view.findViewById(R.id.mptSimulation)


        val options1 = resources.getStringArray(R.array.Simulation)
        var simulate = false

        option1.adapter = ArrayAdapter<String>(activity!!.applicationContext, android.R.layout.simple_list_item_1, options1)

        option1.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onNothingSelected(parent: AdapterView<*>?) {
                return null!!
            }

            override fun onItemSelected(
                parent: AdapterView<*>?,
                view: View?,
                position: Int,
                id: Long
            ) {
                simulate = portfolioSimulation.toString() != options1.get(position).toString()
                portfolioSimulation.clear()
                portfolioSimulation.add(options1.get(position))

            }

        }

        mptBtn.setOnClickListener {

            if (!mptRes.text.contains("Investment Universe:") || simulate) {

                if (portfolio.size < 2) {
                    Toast.makeText(activity, "Error: Select at least 2 stocks from the dropdown!", Toast.LENGTH_SHORT).show()
                } else if (portfolioSimulation.contains("Set Simulation")) {
                    Toast.makeText(activity, "Error: Set simulation value!", Toast.LENGTH_SHORT).show()
                } else {
                    var simulationVal = portfolioSimulation.toString()
                    var mptCache = initMPT(simulationVal)

                    var mptCacheImg = mptCache?.get(0).toString()
                    var mptCacheTxt = mptCache?.get(1).toString()
                    mptRes.text = mptCacheTxt
                    var mptCacheLoad = mptCache?.get(2).toString()

                    if (mptCacheImg != "error") {
                        val intent = Intent(view.context, Graph::class.java)
                        intent.putExtra("res", mptCacheImg)
                        startActivity(intent)
                        simulate = false
                    }

                    if (mptCacheLoad.contains("Quandl API cannot load price data")) {
                        Toast.makeText(activity, mptCacheLoad, Toast.LENGTH_LONG).show()

                    }
                }
            }
        }

        mptClearPort.setOnClickListener {
            portfolio.clear()
            mptRes.text = ""
        }

    }

    fun initMPT(simulationVal: String): MutableList<PyObject>? {
        val python = Python.getInstance()
        val pythonFile = python.getModule("PortfolioMgmt_py")
        return pythonFile.callAttr("MPT", portfolio.toString(), simulationVal).asList()
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_portfoliomgmt, container, false)
    }

    companion object {
        /**
         * Use this factory method to create a new instance of
         * this fragment using the provided parameters.
         *
         * @param param1 Parameter 1.
         * @param param2 Parameter 2.
         * @return A new instance of fragment PortfolioMgmtFragment.
         */
        // TODO: Rename and change types and number of parameters
        @JvmStatic
        fun newInstance(param1: String, param2: String) =
            PortfolioMgmtFragment().apply {
                arguments = Bundle().apply {
                    putString(ARG_PARAM1, param1)
                    putString(ARG_PARAM2, param2)
                }
            }
    }
}