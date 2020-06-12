package controller

import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentManager
import androidx.fragment.app.FragmentPagerAdapter
import view.*


class SupplementalAdapter(fragmentManager: FragmentManager): FragmentPagerAdapter(fragmentManager) {
    override fun getItem(position: Int): Fragment {
        when (position) {
            0 -> return AlgoTradingFragment()
            1 -> return ValueatRiskFragment()
            2 -> return PortfolioMgmtFragment()
            //3 -> return BondValuationFragment()
            3 -> return ValuationsFragment()
            4 -> return MacroDataFragment()
            5 -> return NewsFragment()
            6 -> return AboutFragment()

        }
        return null!!
    }

    override fun getCount(): Int {
        return 7
    }

    override fun getPageTitle(position: Int): CharSequence? {
        when (position) {
            0 -> return "Algo Trading"
            1 -> return "Risk Management"
            2 -> return "Portfolio Optimization"
            //3 -> return "Bond Valuation"
            3 -> return "Option Valuation"
            4 -> return "Macroeconomic Data"
            5 -> return "News"
            6 -> return "About"

        }
        return null

    }

}



