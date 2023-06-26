import BookStore from '@/store/bookStore';
import ReportStore from '@/store/reportStore';
import LoanSlipStore from '@/store/loanSlipStore';
import MemberStore from '@/store/memberStore';
import RuleStore from '@/store/ruleStore';
import OrganizationStore from '@/store/organizationStore';

export default function initializeStores() {
  return {
    bookStore: new BookStore(),
    reportStore: new ReportStore(),
    loanSlipStore: new LoanSlipStore(),
    memberStore: new MemberStore(),
    ruleStore: new RuleStore(),
    organizationStore: new OrganizationStore(),
  };
}
