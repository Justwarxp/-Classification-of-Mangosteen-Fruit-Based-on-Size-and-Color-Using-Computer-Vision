package com.example.manggis.activity

import android.content.Intent
import android.os.Build
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.cardview.widget.CardView
import androidx.core.content.ContextCompat
import com.example.manggis.R

class HomeActivity : AppCompatActivity() {
    private lateinit var cardView2:CardView
    private lateinit var cardView:CardView


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_home)
        hideStatusAndNavigation()
        cardView=findViewById<CardView>(R.id.cardView)
        cardView2=findViewById<CardView>(R.id.cv_dari_tanggal)
        cardView.setOnClickListener{
            startActivity(Intent(this@HomeActivity, AllDataActivity::class.java))
        }
        cardView2.setOnClickListener{
            startActivity(Intent(this@HomeActivity, HistoryActivity::class.java))
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