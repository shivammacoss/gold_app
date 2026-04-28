export const APP_NAME = "SetupFX";

export const NETWORKS = {
  TRC20: { label: "TRON (TRC-20)", color: "text-red-400" },
  ERC20: { label: "Ethereum (ERC-20)", color: "text-blue-400" },
  BEP20: { label: "BSC (BEP-20)", color: "text-yellow-400" },
} as const;

export const TRANSACTION_LABELS: Record<string, { label: string; color: string }> = {
  DEPOSIT: { label: "Deposit", color: "text-green-400" },
  WITHDRAWAL: { label: "Withdrawal", color: "text-red-400" },
  WITHDRAWAL_HOLD: { label: "Withdrawal Hold", color: "text-orange-400" },
  WITHDRAWAL_REFUND: { label: "Refund", color: "text-blue-400" },
  INVESTMENT: { label: "Investment", color: "text-purple-400" },
  INVESTMENT_RETURN: { label: "Principal Return", color: "text-green-400" },
  ROI: { label: "Daily ROI", color: "text-emerald-400" },
  TRANSFER: { label: "Transfer", color: "text-gray-400" },
  FEE: { label: "Fee", color: "text-red-300" },
  BONUS: { label: "Bonus", color: "text-yellow-400" },
};
