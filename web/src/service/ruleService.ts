class RuleService {
  public async getAll(): Promise<any> {
    const response = await fetch('../src/service/rule.json');
    const data = await response.json();
    return data;
  }
}

export default new RuleService();
