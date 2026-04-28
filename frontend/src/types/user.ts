export interface User {
  id: string;
  email: string;
  username: string;
  phone_number: string;
  is_kyc_verified: boolean;
  referral_code: string | null;
  date_joined: string;
}

export interface UserProfile {
  id: string;
  email: string;
  full_name: string;
  avatar: string | null;
  country: string;
  date_of_birth: string | null;
}

export interface LoginResponse {
  access: string;
  refresh: string;
}

export interface RegisterPayload {
  email: string;
  username: string;
  password: string;
  password_confirm: string;
}
