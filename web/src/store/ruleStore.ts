import ruleService from '@/service/ruleService';
import { observable, action } from 'mobx';
import _ from 'lodash';

export interface IRule {
  min_age: number;
  max_age: number;
  time_effective_card: number;
  detail_category: string[];
  detail_type: string[];
  distance_year: number;
  max_items_borrow: number;
  max_day_borrow: number;
}

class RuleStore {
  @observable ruleData: IRule = {} as IRule;
  @observable owner: string = '';
  @observable ruleId: number = 0;

  @action getAll = async () => {
    console.log('Fetching rule data...');
    try {
      const result = await ruleService.getAll();
      this.ruleData = result[0];
      this.owner = result[0].owner;
      this.ruleId = result[0].id;
    } catch (error) {
      console.error('Error fetching rule:', error);
    }
  };

  @action updateRule = async (rule: any) => {
    try {
      const data = {
        ...rule,
        detail_type: this.ruleData.detail_type,
        numbers_category: rule.detail_category.length,
      };
      const result = await ruleService.updateRule(data, this.ruleId);
      this.ruleData = result;
      return result;
    } catch (error) {
      console.error('Error updating rule:', error);
    }
  };

  hasRuleData() {
    return !_.isEmpty(this.ruleData);
  }
}

export default RuleStore;
