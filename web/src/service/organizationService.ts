class Organization {
  public async getAllUser(): Promise<any> {
    const response = await fetch('../src/service/organization.json');
    const data = await response.json();
    return data;
  }
}

export default new Organization();
