import axios from 'axios'

const PAKASIR_BASE = "https://app.pakasir.com/api"

export function generateReffId() {
  const rand = Math.random().toString(36).slice(2, 10).toUpperCase()
  return `TRX-${Date.now()}-${rand}`
}

export async function createdQris(harga, configPakasir) {
  const amount = Number(harga)
  console.log(`[PAKASIR] Lagi bikin QRIS buat nominal ${amount}`)
  
  try {
    const orderId = generateReffId()
    const payload = {
      project: configPakasir.project,
      order_id: orderId,
      amount: amount,
      api_key: configPakasir.apikey
    }
    
    console.log(`[PAKASIR] Kirim request ke API...`)
    const response = await axios.post(`${PAKASIR_BASE}/transactioncreate/qris`, payload, {
      headers: { "Content-Type": "application/json" },
      timeout: 15000
    })
    
    const data = response.data
    
    if (!data || !data.payment) {
      console.log(`[PAKASIR] Gagal: response gak ada payment`)
      return null
    }
    
    const payment = data.payment
    
    console.log(`[PAKASIR] QRIS berhasil dibuat, ID: ${payment.order_id}`)
    
    return {
      idtransaksi: payment.order_id,
      jumlah: payment.total_payment,
      qr_string: payment.payment_number,
      nominal: payment.amount,
      expired_at: new Date(Date.now() + 5 * 60 * 1000)
    }
    
  } catch (e) {
    console.error(`[PAKASIR] Waduh error bang: ${e.response?.data?.message || e.message}`)
    return null
  }
}

export async function cekStatusPakasir(id, amount, apiKey, project) {
  console.log(`[PAKASIR] Lagi ngecek status transaksi ${id}`)
  
  try {
    const url = `${PAKASIR_BASE}/transactiondetail?project=${project}&amount=${amount}&order_id=${id}&api_key=${apiKey}`
    const response = await axios.get(url, { timeout: 10000 })
    const data = response.data
    
    if (data && data.transaction && data.transaction.status === 'completed') {
      console.log(`[PAKASIR] Transaksi ${id} udah lunas bang!`)
      return true
    }
    
    console.log(`[PAKASIR] Transaksi ${id} masih pending bang`)
    return false
    
  } catch (e) {
    if (e.response && e.response.status === 404) {
      console.log(`[PAKASIR] Transaksi ${id} gak ditemukan`)
      return false
    }
    console.error(`[PAKASIR] Gagal ngecek status bang: ${e.message}`)
    return false
  }
}