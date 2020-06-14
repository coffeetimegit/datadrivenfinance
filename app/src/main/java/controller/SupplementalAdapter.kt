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
            3 -> return ValuationsFragment()
            4 -> return BondValuationFragment()
            5 -> return MacroDataFragment()
            6 -> return NewsFragment()
            7 -> return AboutFragment()

        }
        return null!!
    }

    override fun getCount(): Int {
        return 8
    }

    override fun getPageTitle(position: Int): CharSequence? {
        when (position) {
            0 -> return "Algo Trading"
            1 -> return "Risk Management"
            2 -> return "Portfolio Optimization"
            3 -> return "Option Valuation"
            4 -> return "Bond Valuation"
            5 -> return "Macroeconomic Data"
            6 -> return "News"
            7 -> return "About"

        }
        return null

    }

}



