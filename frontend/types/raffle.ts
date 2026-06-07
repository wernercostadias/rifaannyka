export type Raffle = {
  id: number
  title: string
  description: string
  beneficiary_name: string
  image?: string
  goal_amount: string
  price_per_number: string
  raised_amount: string
  progress_percentage: string
  sold_count: number
  total_numbers: number
}

export type RaffleNumber = {
  id: number
  number: number
  status: string
  owner_name?: string
}

export type PublicPurchase = {
  buyer_name: string
  buyer_phone: string
  numbers: number[]
  status: string
  created_at: string
}

export type LookupPurchase = {
  reference: string
  buyer_name: string
  buyer_phone: string
  numbers: number[]
  status: string
  status_label: string
  created_at: string
}

export type PurchaseResponse = {
  reference: string
  raffle: number
  buyer: {
    first_name: string
    last_name: string
    email: string
    phone: string
    cpf: string
  }
  numbers: number[]
  total_amount: string
  status: string
  reservation_expires_at: string
  payment_reference: string
}

export type PaymentResponse = {
  id: number
  purchase: number
  provider: string
  amount: string
  status: string
  external_id: string
  qr_code: string
  qr_code_text: string
  paid_at: string | null
}

export type BuyerFormData = {
  full_name: string
  phone: string
  cpf: string
}

export type BuyerFormErrors = {
  full_name: string
  phone: string
  cpf: string
}
