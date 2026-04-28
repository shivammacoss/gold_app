export type TransactionType =
  | "DEPOSIT"
  | "WITHDRAWAL"
  | "WITHDRAWAL_HOLD"
  | "WITHDRAWAL_REFUND"
  | "INVESTMENT"
  | "INVESTMENT_RETURN"
  | "ROI"
  | "TRANSFER"
  | "FEE"
  | "BONUS";

export interface Transaction {
  id: string;
  user_email: string;
  tx_type: TransactionType;
  amount: string;
  reference_id: string;
  description: string;
  created_at: string;
}
