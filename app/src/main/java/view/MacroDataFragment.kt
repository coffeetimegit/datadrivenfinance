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
import kotlinx.android.synthetic.main.fragment_macrodata.*


// TODO: Rename parameter arguments, choose names that match
// the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
private const val ARG_PARAM1 = "param1"
private const val ARG_PARAM2 = "param2"

/**
 * A simple [Fragment] subclass.
 * Use the [MacroDataFragment.newInstance] factory method to
 * create an instance of this fragment.
 */
class MacroDataFragment : Fragment() {
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

    var countryList = mutableSetOf<String>()
    var dataType = String()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        lateinit var option: Spinner
        lateinit var result: TextView

        option = view!!.findViewById(R.id.selectCountries)
        result = view!!.findViewById(R.id.countries)

        val options = getResources().getStringArray(R.array.IS03List)

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
                countryList.add(options.get(position))
                if (countryList.size > 1 && countryList.contains("Select Country")) {
                    countryList.remove("Select Country")
                }
                result.text = countryList.toString()
            }

        }

        val errorMsg = "Error: Select at least 1 country from the dropdown!"

        populationAbsBtn.setOnClickListener {

            if (countries.text.contains("Select Country") || countries.text == "") {
                Toast.makeText(activity, errorMsg, Toast.LENGTH_SHORT).show()
            } else {
                dataType = "population"
                var macroCache = initMACROABS()
                var macroCacheImg = macroCache?.get(0).toString()
                var macroCacheError = macroCache?.get(1).toString()

                if (macroCacheImg.contains("error")) {
                    Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                } else {
                    val intent = Intent(view.context, Graph::class.java)
                    intent.putExtra("res", macroCacheImg)
                    startActivity(intent)
                    if (macroCacheError.contains("Quandl API cannot load")) {
                        Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                    }
                }
            }
        }


        gdpAbsBtn.setOnClickListener {

            if (countries.text.contains("Select Country") || countries.text == "") {
                Toast.makeText(activity, errorMsg, Toast.LENGTH_SHORT).show()
            } else {
                dataType = "gdp"
                var macroCache = initMACROABS()
                var macroCacheImg = macroCache?.get(0).toString()
                var macroCacheError = macroCache?.get(1).toString()

                if (macroCacheImg.contains("error")) {
                    Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                } else {
                    val intent = Intent(view.context, Graph::class.java)
                    intent.putExtra("res", macroCacheImg)
                    startActivity(intent)
                    if (macroCacheError.contains("Quandl API cannot load")) {
                        Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                    }
                }
            }
        }


        govSpendingAbsBtn.setOnClickListener {

            if (countries.text.contains("Select Country") || countries.text == "") {
                Toast.makeText(activity, errorMsg, Toast.LENGTH_SHORT).show()
            } else {
                dataType = "govspending"
                var macroCache = initMACROABS()
                var macroCacheImg = macroCache?.get(0).toString()
                var macroCacheError = macroCache?.get(1).toString()

                if (macroCacheImg.contains("error")) {
                    Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                } else {
                    val intent = Intent(view.context, Graph::class.java)
                    intent.putExtra("res", macroCacheImg)
                    startActivity(intent)
                    if (macroCacheError.contains("Quandl API cannot load")) {
                        Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                    }
                }
            }
        }


        debtAbsBtn.setOnClickListener {

            if (countries.text.contains("Select Country") || countries.text == "") {
                Toast.makeText(activity, errorMsg, Toast.LENGTH_SHORT).show()
            } else {
                dataType = "debt"
                var macroCache = initMACROABS()
                var macroCacheImg = macroCache?.get(0).toString()
                var macroCacheError = macroCache?.get(1).toString()

                if (macroCacheImg.contains("error")) {
                    Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                } else {
                    val intent = Intent(view.context, Graph::class.java)
                    intent.putExtra("res", macroCacheImg)
                    startActivity(intent)
                    if (macroCacheError.contains("Quandl API cannot load")) {
                        Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                    }
                }
            }
        }


        unemploymentAbsBtn.setOnClickListener {

            if (countries.text.contains("Select Country") || countries.text == "") {
                Toast.makeText(activity, errorMsg, Toast.LENGTH_SHORT).show()
            } else {
                dataType = "unemployment"
                var macroCache = initMACROABS()
                var macroCacheImg = macroCache?.get(0).toString()
                var macroCacheError = macroCache?.get(1).toString()

                if (macroCacheImg.contains("error")) {
                    Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                } else {
                    val intent = Intent(view.context, Graph::class.java)
                    intent.putExtra("res", macroCacheImg)
                    startActivity(intent)
                    if (macroCacheError.contains("Quandl API cannot load")) {
                        Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                    }
                }
            }
        }


        importAbsBtn.setOnClickListener {

            if (countries.text.contains("Select Country") || countries.text == "") {
                Toast.makeText(activity, errorMsg, Toast.LENGTH_SHORT).show()
            } else {
                dataType = "import"
                var macroCache = initMACROABS()
                var macroCacheImg = macroCache?.get(0).toString()
                var macroCacheError = macroCache?.get(1).toString()

                if (macroCacheImg.contains("error")) {
                    Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                } else {
                    val intent = Intent(view.context, Graph::class.java)
                    intent.putExtra("res", macroCacheImg)
                    startActivity(intent)
                    if (macroCacheError.contains("Quandl API cannot load")) {
                        Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                    }
                }
            }
        }


        exportAbsBtn.setOnClickListener {

            if (countries.text.contains("Select Country") || countries.text == "") {
                Toast.makeText(activity, errorMsg, Toast.LENGTH_SHORT).show()
            } else {
                dataType = "export"
                var macroCache = initMACROABS()
                var macroCacheImg = macroCache?.get(0).toString()
                var macroCacheError = macroCache?.get(1).toString()

                if (macroCacheImg.contains("error")) {
                    Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                } else {
                    val intent = Intent(view.context, Graph::class.java)
                    intent.putExtra("res", macroCacheImg)
                    startActivity(intent)
                    if (macroCacheError.contains("Quandl API cannot load")) {
                        Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                    }
                }
            }
        }


        populationRelBtn.setOnClickListener {

            if (countries.text.contains("Select Country") || countries.text == "") {
                Toast.makeText(activity, errorMsg, Toast.LENGTH_SHORT).show()
            } else {
                dataType = "population"
                var macroCache = initMACROREL()
                var macroCacheImg = macroCache?.get(0).toString()
                var macroCacheError = macroCache?.get(1).toString()

                if (macroCacheImg.contains("error")) {
                    Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                } else {
                    val intent = Intent(view.context, Graph::class.java)
                    intent.putExtra("res", macroCacheImg)
                    startActivity(intent)
                    if (macroCacheError.contains("Quandl API cannot load")) {
                        Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                    }
                }
            }
        }


        gdpRelBtn.setOnClickListener {

            if (countries.text.contains("Select Country") || countries.text == "") {
                Toast.makeText(activity, errorMsg, Toast.LENGTH_SHORT).show()
            } else {
                dataType = "gdp"
                var macroCache = initMACROREL()
                var macroCacheImg = macroCache?.get(0).toString()
                var macroCacheError = macroCache?.get(1).toString()

                if (macroCacheImg.contains("error")) {
                    Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                } else {
                    val intent = Intent(view.context, Graph::class.java)
                    intent.putExtra("res", macroCacheImg)
                    startActivity(intent)
                    if (macroCacheError.contains("Quandl API cannot load")) {
                        Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                    }
                }
            }
        }


        govSpendingRelBtn.setOnClickListener {

            if (countries.text.contains("Select Country") || countries.text == "") {
                Toast.makeText(activity, errorMsg, Toast.LENGTH_SHORT).show()
            } else {
                dataType = "govspending"
                var macroCache = initMACROREL()
                var macroCacheImg = macroCache?.get(0).toString()
                var macroCacheError = macroCache?.get(1).toString()

                if (macroCacheImg.contains("error")) {
                    Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                } else {
                    val intent = Intent(view.context, Graph::class.java)
                    intent.putExtra("res", macroCacheImg)
                    startActivity(intent)
                    if (macroCacheError.contains("Quandl API cannot load")) {
                        Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                    }
                }
            }
        }


        debtRelBtn.setOnClickListener {

            if (countries.text.contains("Select Country") || countries.text == "") {
                Toast.makeText(activity, errorMsg, Toast.LENGTH_SHORT).show()
            } else {
                dataType = "debt"
                var macroCache = initMACROREL()
                var macroCacheImg = macroCache?.get(0).toString()
                var macroCacheError = macroCache?.get(1).toString()

                if (macroCacheImg.contains("error")) {
                    Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                } else {
                    val intent = Intent(view.context, Graph::class.java)
                    intent.putExtra("res", macroCacheImg)
                    startActivity(intent)
                    if (macroCacheError.contains("Quandl API cannot load")) {
                        Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                    }
                }
            }
        }


        unemploymentRelBtn.setOnClickListener {

            if (countries.text.contains("Select Country") || countries.text == "") {
                Toast.makeText(activity, errorMsg, Toast.LENGTH_SHORT).show()
            } else {
                dataType = "unemployment"
                var macroCache = initMACROREL()
                var macroCacheImg = macroCache?.get(0).toString()
                var macroCacheError = macroCache?.get(1).toString()

                if (macroCacheImg.contains("error")) {
                    Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                } else {
                    val intent = Intent(view.context, Graph::class.java)
                    intent.putExtra("res", macroCacheImg)
                    startActivity(intent)
                    if (macroCacheError.contains("Quandl API cannot load")) {
                        Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                    }
                }
            }
        }


        importRelBtn.setOnClickListener {

            if (countries.text.contains("Select Country") || countries.text == "") {
                Toast.makeText(activity, errorMsg, Toast.LENGTH_SHORT).show()
            } else {
                dataType = "import"
                var macroCache = initMACROREL()
                var macroCacheImg = macroCache?.get(0).toString()
                var macroCacheError = macroCache?.get(1).toString()

                if (macroCacheImg.contains("error")) {
                    Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                } else {
                    val intent = Intent(view.context, Graph::class.java)
                    intent.putExtra("res", macroCacheImg)
                    startActivity(intent)
                    if (macroCacheError.contains("Quandl API cannot load")) {
                        Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                    }
                }
            }
        }


        exportRelBtn.setOnClickListener {

            if (countries.text.contains("Select Country") || countries.text == "") {
                Toast.makeText(activity, errorMsg, Toast.LENGTH_SHORT).show()
            } else {
                dataType = "export"
                var macroCache = initMACROREL()
                var macroCacheImg = macroCache?.get(0).toString()
                var macroCacheError = macroCache?.get(1).toString()

                if (macroCacheImg.contains("error")) {
                    Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                } else {
                    val intent = Intent(view.context, Graph::class.java)
                    intent.putExtra("res", macroCacheImg)
                    startActivity(intent)
                    if (macroCacheError.contains("Quandl API cannot load")) {
                        Toast.makeText(activity, macroCacheError, Toast.LENGTH_LONG).show()
                    }
                }
            }
        }


        countryClear.setOnClickListener {
            countryList.clear()
            countries.text = ""
        }


    }

    private fun initMACROABS(): MutableList<PyObject>? {
        var abs = true
        val python = Python.getInstance()
        val pythonFile = python.getModule("MacroData_py")
        return pythonFile.callAttr("MacroData", countries.text.toString(),
                                                     dataType, abs).asList()
    }

    private fun initMACROREL(): MutableList<PyObject>? {
        var abs = false
        val python = Python.getInstance()
        val pythonFile = python.getModule("MacroData_py")
        return pythonFile.callAttr("MacroData", countries.text.toString(),
            dataType, abs).asList()
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_macrodata, container, false)
    }

    companion object {
        /**
         * Use this factory method to create a new instance of
         * this fragment using the provided parameters.
         *
         * @param param1 Parameter 1.
         * @param param2 Parameter 2.
         * @return A new instance of fragment MacroDataFragment.
         */
        // TODO: Rename and change types and number of parameters
        @JvmStatic
        fun newInstance(param1: String, param2: String) =
            MacroDataFragment().apply {
                arguments = Bundle().apply {
                    putString(ARG_PARAM1, param1)
                    putString(ARG_PARAM2, param2)
                }
            }
    }
}