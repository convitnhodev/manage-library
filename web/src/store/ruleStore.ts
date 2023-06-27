import ruleService from '@/service/ruleService';
import { observable, action } from 'mobx';
import _ from 'lodash';

export interface IRule {
  minMemberAge: number;
  maxMemberAge: number;
  periodValidCard: number;
  categoryBooks: string[];
  publicationYearGap: number;
  maxBookCanBorrow: number;
  maxDayCanBorrow: number;
}

class RuleStore {
  @observable ruleData: IRule = {} as IRule;

  @action getAll = async () => {
    console.log('Fetching rule data...');
    try {
      const result = await ruleService.getAll();
      this.ruleData = result.rule;
    } catch (error) {
      console.error('Error fetching rule:', error);
    }
  };

  hasRuleData() {
    return !_.isEmpty(this.ruleData);
  }
}

export default RuleStore;
