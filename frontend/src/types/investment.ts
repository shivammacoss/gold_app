export interface InvestmentPlan {
  id: string;
  name: string;
  description: string;
  min_amount: string;
  max_amount: string;
  daily_roi_percent: string;
  duration_days: number;
  is_active: boolean;
}

export interface UserInvestment {
  id: string;
  user_email: string;
  plan: string;
  plan_name: string;
  wallet: string;
  amount: string;
  total_earned: string;
  daily_earning: string;
  days_completed: number;
  status: "ACTIVE" | "COMPLETED" | "CANCELLED";
  started_at: string;
  expires_at: string;
  created_at: string;
}
