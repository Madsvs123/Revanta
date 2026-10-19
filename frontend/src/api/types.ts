export type User = {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  display_name: string;
};

export type Organization = {
  id: string;
  name: string;
  slug: string;
  default_currency: string;
  industry: string;
};

export type Company = {
  id: string;
  name: string;
  domain: string;
  stage: string;
  country: string;
  mrr: string;
  balance: string;
  credit_balance: string;
  health_score: string;
  notes?: string;
  contacts?: Contact[];
  billing_profiles?: BillingProfile[];
};

export type Contact = {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  title: string;
  is_primary: boolean;
};

export type BillingProfile = {
  id: string;
  currency: string;
  invoice_email: string;
  country: string;
};

export type Product = {
  id: string;
  name: string;
  sku: string;
  product_type: string;
  unit_label: string;
  is_active: boolean;
  plans: Plan[];
};

export type Plan = {
  id: string;
  product: string;
  name: string;
  code: string;
  interval: string;
  trial_days: number;
  setup_fee: string;
  minimum_commitment: string;
  billing_model: string;
  tiers?: { id: string; unit_amount: string; up_to: number | null }[];
};

export type Coupon = {
  id: string;
  name: string;
  code: string;
  percent_off?: string;
  amount_off?: string;
  duration: string;
};

export type Subscription = {
  id: string;
  company: string;
  company_name: string;
  plan: string;
  plan_name: string;
  status: string;
  quantity: number;
  currency: string;
  unit_amount: string;
  mrr: string;
  current_period_start: string;
  current_period_end: string;
  cancel_at_period_end: boolean;
  items?: { id: string; description: string; quantity: number; unit_amount: string }[];
  amendments?: { id: string; amendment_type: string; summary: string; created_at: string }[];
};

export type Invoice = {
  id: string;
  company: string;
  company_name: string;
  number: string;
  status: string;
  currency: string;
  issue_date: string;
  due_date: string;
  total: string;
  amount_due: string;
  amount_paid: string;
  tax_total: string;
  credit_total: string;
  lines?: { id: string; description: string; amount: string; quantity: string }[];
};

export type Payment = {
  id: string;
  company_name: string;
  invoice_number: string;
  amount: string;
  currency: string;
  status: string;
  provider: string;
  attempt_count: number;
  failure_message: string;
};

export type UsagePeriod = {
  id: string;
  metric_name: string;
  company_name: string;
  period_start: string;
  period_end: string;
  quantity: string;
  billable_quantity: string;
  amount: string;
};

export type DunningCase = {
  id: string;
  company_name: string;
  invoice_number: string;
  status: string;
  current_step: number;
  next_action_at: string;
};

export type Contract = {
  id: string;
  company_name: string;
  name: string;
  number: string;
  status: string;
  start_date: string;
  end_date: string;
  acv: string;
};

export type Renewal = {
  id: string;
  company_name: string;
  contract_name: string;
  stage: string;
  target_date: string;
  expected_acv: string;
  probability: number;
  weighted: number;
};

export type Snapshot = {
  mrr: string;
  arr: string;
  new_mrr: string;
  expansion_mrr: string;
  contraction_mrr: string;
  churned_mrr: string;
  net_new_mrr: string;
  nrr: string;
  ltv: string;
  failed_payments: number;
  collections_balance: string;
  active_customers: number;
  as_of: string;
};

export type Notification = {
  id: string;
  category: string;
  title: string;
  created_at: string;
  read_at?: string | null;
};
