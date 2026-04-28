export interface Wallet {
  id: string;
  user_email: string;
  network: "TRC20" | "ERC20" | "BEP20";
  address: string;
  balance: string;
  is_active: boolean;
  created_at: string;
}
