package com.example.manggis.activity

import android.annotation.SuppressLint
import android.app.DatePickerDialog
import android.app.Dialog
import android.os.Build
import android.os.Bundle
import android.transition.AutoTransition
import android.transition.TransitionManager
import android.util.Log
import android.view.View
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.cardview.widget.CardView
import androidx.constraintlayout.widget.ConstraintLayout
import androidx.core.content.ContextCompat
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout
import com.example.manggis.R
import com.example.manggis.adapters.HistoryAdapter
import com.example.manggis.databinding.ActivityHistoryBinding
import com.example.manggis.databinding.DialogDeleteAllSessionsBinding
import com.example.manggis.repository.SessionRepository
import com.example.manggis.retrofit.ApiService
import com.example.manggis.viewModel.LatestSesionViewModel
import com.example.manggis.viewModel.factory.LatestSessionFactory
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Locale

class HistoryActivity : AppCompatActivity() {
    private lateinit var binding: ActivityHistoryBinding

    private lateinit var backButton:ImageView

    private lateinit var rc_history: RecyclerView
    private lateinit var historyAdapter: HistoryAdapter

    private lateinit var img_delete_session:ImageView
    private lateinit var img_try_filter:ImageView
    private lateinit var hiddenFilter: ConstraintLayout
    private lateinit var baseFilterCardView: CardView
    private lateinit var sw_refresh:SwipeRefreshLayout
    private lateinit var tv_date_start:TextView
    private lateinit var tv_date_end:TextView
    private lateinit var dateStartPickerDialog:DatePickerDialog
    private lateinit var dateEndPickerDialog:DatePickerDialog
    private lateinit var tv_filter:TextView

    private lateinit var latestSesionViewModel: LatestSesionViewModel
    private val apiService=ApiService.getInstance()
    private var paginationJob: Job? = null

    private lateinit var dialogDeleteAllSessionsBinding: DialogDeleteAllSessionsBinding
    private lateinit var dialogDeleteAllSessionsBindingPopUp:Dialog

    @SuppressLint("MissingInflatedId")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding= ActivityHistoryBinding.inflate(layoutInflater)
        setContentView(binding.root)
        hideStatusAndNavigation()
        initializeComponent(binding)
    }

    fun initializeComponent(binding: ActivityHistoryBinding){
        latestSesionViewModel=ViewModelProvider(this,LatestSessionFactory(SessionRepository(apiService)))[LatestSesionViewModel::class.java]

        backButton=binding.backButton

        img_try_filter=binding.imgTrayFilter
        hiddenFilter=binding.hiddenFilter
        baseFilterCardView=binding.baseFilterCardView
        img_delete_session=binding.imgDeleteSession
        dialogDeleteAllSessionsBinding=DialogDeleteAllSessionsBinding.inflate(layoutInflater)
        dialogDeleteAllSessionsBindingPopUp= Dialog(binding.root.context)
        dialogDeleteAllSessionsBindingPopUp.window?.setBackgroundDrawableResource(android.R.color.transparent)
        dialogDeleteAllSessionsBindingPopUp.setContentView(dialogDeleteAllSessionsBinding.root)

        sw_refresh=binding.swRefresh
        rc_history=binding.rcHistory
        historyAdapter= HistoryAdapter()
        rc_history.apply {
            layoutManager=LinearLayoutManager(binding.root.context)
            adapter=this@HistoryActivity.historyAdapter
        }
        paginationJob=lifecycleScope.launch {
            latestSesionViewModel.getSessions().collectLatest{
//                Log.d("testx","hey")
                sw_refresh.isRefreshing = false
                historyAdapter.submitData(it)
            }
        }
        sw_refresh.setOnRefreshListener {
            historyAdapter.refresh()
        }

        tv_date_start=binding.tvDateStart
        tv_date_end=binding.tvDateEnd
        tv_filter=binding.tvFilter
        val calendar = Calendar.getInstance()
        val year = calendar.get(Calendar.YEAR)
        val month = calendar.get(Calendar.MONTH)
        val day = calendar.get(Calendar.DAY_OF_MONTH)
        dateStartPickerDialog = DatePickerDialog(
            binding.root.context,
            { view, year, monthOfYear, dayOfMonth ->
                val formattedDate = String.format("%02d/%02d/%04d", dayOfMonth, monthOfYear + 1, year)
                tv_date_start.text = formattedDate
            },
            year,
            month,
            day
        )
        dateStartPickerDialog.setOnCancelListener {
            tv_date_start.text="null"
        }
        dateEndPickerDialog = DatePickerDialog(
            binding.root.context,
            { view, year, monthOfYear, dayOfMonth ->
                val formattedDate = String.format("%02d/%02d/%04d", dayOfMonth, monthOfYear + 1, year)
                tv_date_end.text = formattedDate
            },
            year,
            month,
            day
        )
        dateEndPickerDialog.setOnCancelListener {
            tv_date_end.text="null"
        }

        img_try_filter.setOnClickListener {
            if(hiddenFilter.visibility== View.GONE){
                TransitionManager.beginDelayedTransition(baseFilterCardView,AutoTransition())
                TransitionManager.beginDelayedTransition(sw_refresh,AutoTransition())
                img_try_filter.setImageResource(R.drawable.icon_arrow_up)
                hiddenFilter.visibility=View.VISIBLE
            }
            else{
                TransitionManager.beginDelayedTransition(baseFilterCardView,AutoTransition())
                TransitionManager.beginDelayedTransition(sw_refresh,AutoTransition())
                img_try_filter.setImageResource(R.drawable.icon_arrow_down)
                hiddenFilter.visibility=View.GONE
            }
        }
        tv_date_start.setOnClickListener {
            val calendar = Calendar.getInstance()
            if(tv_date_start.text!="null"){
                val date = SimpleDateFormat("dd/MM/yyyy", Locale.getDefault()).parse(
                    tv_date_start.text.toString()
                )
                calendar.time = date
            }
            val year = calendar.get(Calendar.YEAR)
            val month = calendar.get(Calendar.MONTH)
            val day = calendar.get(Calendar.DAY_OF_MONTH)
            dateStartPickerDialog.updateDate(year,month,day)
            dateStartPickerDialog.show()
        }
        tv_date_end.setOnClickListener {
            val calendar = Calendar.getInstance()
            if(tv_date_end.text!="null"){
                val date = SimpleDateFormat("dd/MM/yyyy", Locale.getDefault()).parse(
                    tv_date_end.text.toString()
                )
                calendar.time = date
            }
            val year = calendar.get(Calendar.YEAR)
            val month = calendar.get(Calendar.MONTH)
            val day = calendar.get(Calendar.DAY_OF_MONTH)
            dateEndPickerDialog.updateDate(year,month,day)
            dateEndPickerDialog.show()
        }
        backButton.setOnClickListener {
            super.onBackPressed()
        }
        dialogDeleteAllSessionsBinding.btnDeleteSessions.setOnClickListener {
            lifecycleScope.launch{
                if(latestSesionViewModel.deleteSessions()){
                    sw_refresh.isRefreshing=true
                    historyAdapter.refresh()
                    paginationJob!!.cancel()
                    paginationJob=lifecycleScope.launch {
                        latestSesionViewModel.getSessions().collectLatest{
                            sw_refresh.isRefreshing = false
                            historyAdapter.submitData(it)
                        }
                    }
                    dialogDeleteAllSessionsBindingPopUp.dismiss()
                    Toast.makeText(binding.root.context,"Sessions Deleted",Toast.LENGTH_SHORT).show()
                }
            }
        }
        dialogDeleteAllSessionsBinding.btnKembaliSession3.setOnClickListener {
            dialogDeleteAllSessionsBindingPopUp.dismiss()
        }
        img_delete_session.setOnClickListener {
            dialogDeleteAllSessionsBindingPopUp.show()

        }
        tv_filter.setOnClickListener {
            if(tv_date_end.text!="null" && tv_date_start.text!="null"){
                sw_refresh.isRefreshing=true
                historyAdapter.refresh()
                paginationJob!!.cancel()
                paginationJob=lifecycleScope.launch {
                    latestSesionViewModel.getSessions(tv_date_start.text.toString(),tv_date_end.text.toString()).collectLatest{
                        sw_refresh.isRefreshing = false
                        historyAdapter.submitData(it)
                    }
                }
            }
            else if(tv_date_end.text=="null" && tv_date_start.text=="null"){
                sw_refresh.isRefreshing=true
                historyAdapter.refresh()
                paginationJob!!.cancel()
                paginationJob=lifecycleScope.launch {
                    latestSesionViewModel.getSessions().collectLatest{
                        sw_refresh.isRefreshing = false
                        historyAdapter.submitData(it)
                    }
                }
            }
            else{
                Toast.makeText(binding.root.context,"Filter Tanggal Harus Terisi Start dan End Tanggal",Toast.LENGTH_SHORT).show()
            }
        }
    }
    fun hideStatusAndNavigation(){
        if (Build.VERSION.SDK_INT >= 21) {
            window.statusBarColor = ContextCompat.getColor(this, R.color.colorPrimary)
            window.navigationBarColor = ContextCompat.getColor(this, R.color.colorPrimary)
//            window.decorView.systemUiVisibility = (View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR)

        }
    }
}