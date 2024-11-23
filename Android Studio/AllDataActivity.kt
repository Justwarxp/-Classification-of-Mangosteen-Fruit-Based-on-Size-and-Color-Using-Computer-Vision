package com.example.manggis.activity

import android.annotation.SuppressLint
import android.app.Dialog
import android.graphics.Color
import android.os.Build
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.lifecycleScope
import com.example.manggis.R
import com.example.manggis.databinding.ActivityAllDataBinding
import com.example.manggis.databinding.DialogNewSessionBinding
import com.example.manggis.databinding.DialogStopSessionBinding
import com.example.manggis.repository.SessionRepository
import com.example.manggis.retrofit.ApiService
import com.example.manggis.viewModel.LatestSesionViewModel
import com.example.manggis.viewModel.factory.LatestSessionFactory
import kotlinx.coroutines.launch


class AllDataActivity : AppCompatActivity() {
    private lateinit var binding: ActivityAllDataBinding

    private lateinit var latestSesionViewModel: LatestSesionViewModel

    private lateinit var backButton:ImageView
    private lateinit var btn_new:Button
    private lateinit var btn_stop:Button

    private lateinit var dialogNewSession:DialogNewSessionBinding
    private lateinit var dialogStopSession:DialogStopSessionBinding
    private lateinit var  dialogNewSessionPopUp: Dialog
    private lateinit var  dialogStopSessionPopUp: Dialog

    private val apiService=ApiService.getInstance()
    private lateinit var tv_start_date:TextView
    private lateinit var tv_end_date:TextView
    private lateinit var tv_s1:TextView
    private lateinit var tv_s2:TextView
    private lateinit var tv_s3:TextView
    private lateinit var tv_sj:TextView
    private lateinit var tv_se:TextView
    private lateinit var tv_bs:TextView


    @RequiresApi(Build.VERSION_CODES.O)
    @SuppressLint("MissingInflatedId")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding=ActivityAllDataBinding.inflate(layoutInflater)
        setContentView(binding.root)
        initializeComponent(binding)
        observers()
        hideStatusAndNavigation()

    }

    fun initializeComponent(binding:ActivityAllDataBinding){
        latestSesionViewModel = ViewModelProvider(this,LatestSessionFactory(SessionRepository(apiService)))[LatestSesionViewModel::class.java]

        btn_new=binding.btnNew
        btn_stop=binding.btnStop
        backButton=binding.backButton

        dialogNewSession = DialogNewSessionBinding.inflate(layoutInflater)
        dialogStopSession=DialogStopSessionBinding.inflate(layoutInflater)
        dialogNewSessionPopUp= Dialog(binding.root.context);
        dialogStopSessionPopUp= Dialog(binding.root.context);
        dialogNewSessionPopUp.window?.setBackgroundDrawableResource(android.R.color.transparent)
        dialogStopSessionPopUp.window?.setBackgroundDrawableResource(android.R.color.transparent)
        dialogNewSessionPopUp.setContentView(dialogNewSession.root)
        dialogStopSessionPopUp.setContentView(dialogStopSession.root)
        dialogNewSession.btnNewSession.setOnClickListener { // get count from text view
            lifecycleScope.launch {
                if (latestSesionViewModel.startSession()) {
                    Toast.makeText(this@AllDataActivity, "Session start successfully", Toast.LENGTH_SHORT).show()
                } else {
                    Toast.makeText(this@AllDataActivity, "Failed to start the session", Toast.LENGTH_SHORT).show()
                }
                dialogNewSessionPopUp.dismiss()
            }
        }
        dialogNewSession.btnKembaliSession2.setOnClickListener { // get count from text view
            dialogNewSessionPopUp.dismiss()
        }
        dialogStopSession.btnStopSession.setOnClickListener {
            lifecycleScope.launch {
                if (latestSesionViewModel.stopSession()) {
                    Toast.makeText(this@AllDataActivity, "Session stopped successfully", Toast.LENGTH_SHORT).show()
                } else {
                    Toast.makeText(this@AllDataActivity, "Failed to stop the session", Toast.LENGTH_SHORT).show()
                }
                dialogStopSessionPopUp.dismiss()
            }
        }
        dialogStopSession.btnKembaliSession.setOnClickListener {
            dialogStopSessionPopUp.dismiss()
        }

        tv_start_date=binding.tvStartDate
        tv_end_date=binding.tvEndDate
        tv_s1=binding.tvS1
        tv_s2=binding.tvS2
        tv_s3=binding.tvS3
        tv_sj=binding.tvSj
        tv_se=binding.tvSe
        tv_bs=binding.tvBs

        backButton.setOnClickListener {
            super.onBackPressed()
        }
        btn_new.setOnClickListener {
            dialogNewSessionPopUp.show()

        }
        btn_stop.setOnClickListener {
            dialogStopSessionPopUp.show()
        }
    }

    @SuppressLint("SetTextI18n")
    @RequiresApi(Build.VERSION_CODES.O)
    fun observers(){
//        latest
        latestSesionViewModel.lastest_session.observe(/* owner = */ this) {
            tv_start_date.text = "Date start : ${
                latestSesionViewModel.reformatDateTime(
                    latestSesionViewModel.lastest_session.value!!.created_at
                )
            }"
            if (latestSesionViewModel.lastest_session.value!!.state=="ended"){
                tv_end_date.text = "Date end : ${
                    latestSesionViewModel.reformatDateTime(
                        latestSesionViewModel.lastest_session.value!!.updated_at
                    )
                }"
                btn_stop.isEnabled=false
            }
            else{
                btn_stop.isEnabled=true
                tv_end_date.text = "Date end : Still Going"
            }
            tv_s1.text= latestSesionViewModel.lastest_session.value!!.sort_result!!.super_1.toString()
            tv_s2.text= latestSesionViewModel.lastest_session.value!!.sort_result!!.super_2.toString()
            tv_s3.text= latestSesionViewModel.lastest_session.value!!.sort_result!!.super_3.toString()
            tv_sj.text= latestSesionViewModel.lastest_session.value!!.sort_result!!.super_jumbo.toString()
            tv_se.text= latestSesionViewModel.lastest_session.value!!.sort_result!!.super_export.toString()
            tv_bs.text= latestSesionViewModel.lastest_session.value!!.sort_result!!.bs.toString()

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