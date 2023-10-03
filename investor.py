import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

class Investor:
    def __init__(self, age, starting_401k_principle, starting_non401k_principle, amnt_invst_401k_percentage, amnt_invst_non401k, amnt_invst_non401k_increase, salary,
                salary_increase, years_to_sim, expected_401k_return, expected_non401k_return, profit_share_percentage, company_401k_investment_per, retirement_age, retirement_distrobution):
                self.age = age
                self.principal_401k = starting_401k_principle
                self.principal_non401k = starting_non401k_principle

                self.per_inv_401k = amnt_invst_401k_percentage
                self.amnt_inv_non401k = amnt_invst_non401k
                self.amnt_invst_non401k_increase = amnt_invst_non401k_increase

                self.salary = salary
                self.salary_increase = salary_increase

                self.sim_years = years_to_sim

                self.expected_401k_return = expected_401k_return
                self.expected_non401k_return = expected_non401k_return

                self.profit_share = profit_share_percentage
                self.company_401k_investment = company_401k_investment_per

                self.retirement_age = retirement_age
                self.retirement_distrobution = retirement_distrobution

                self.max_401k_personal = 23000
                self.max_401k_total = 60000
                self.overage = 0
                self.dollar_value = 1

    def check_contributions(self):
        overage = 0
        monthly_contribution = 0

        yearly_investment = self.return_401k_contribution_yr()
        profit_share = self.return_profit_share_yr()
        company_investment = self.return_401k_contribution_yr_company()

        if yearly_investment + profit_share + company_investment > self.max_401k_total:
            monthly_contribution = (self.max_401k_total - profit_share) / 12
            if monthly_contribution < 0:
                overage = yearly_investment
            elif yearly_investment > self.max_401k_personal:
                overage = yearly_investment - self.max_401k_personal

        elif yearly_investment > self.max_401k_personal:
            monthly_contribution = (self.max_401k_personal / 12) + (company_investment / 12)
        
        self.max_401k_personal += 500
        self.max_401k_total += 1500

        return monthly_contribution, overage

    def calculate_outside_investments(self, overage):
        weekly_investment = self.amnt_inv_non401k + (overage / 12)
        self.principal_non401k += (self.amnt_inv_non401k * 52) + overage
        self.amnt_inv_non401k += self.amnt_inv_non401k * self.amnt_invst_non401k_increase
        return weekly_investment * 4
    
    def return_401k_contribution_yr(self):
        return self.per_inv_401k * self.salary

    def return_401k_contribution_yr_company(self):
        return self.company_401k_investment * self.salary

    def return_profit_share_yr(self):
        return self.profit_share * self.salary

    def stock_market_invest(self, weekly_investment, total_investments, exepected_return_rate):
        yearly_total = weekly_investment * 52
        total_investments += yearly_total
        total_investments += self.yearly_interest(total_investments, exepected_return_rate)
        return total_investments

    def yearly_interest(self, principal, rate):
        return principal * rate

    def dollar_value_calc(self):
        self.dollar_value -= self.dollar_value * .02
        return

    def salary_bump(self):
        self.salary += self.salary * self.salary_increase
        return
    
    def invest(self):
        months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"]
        total_outside_investments =self.principal_non401k
        total = self.principal_401k

        for i in range(self.sim_years):
            if self.age >= self.retirement_age:
                self.age += 1
                # congrats, you're retired
                total_outside_investments += self.yearly_interest(total_outside_investments, self.expected_non401k_return)
                monthly_contribution = 0
                monthly_outside_contribution = 0
                overage = 0
                # change portfolio to risk-adverse
                self.expected_non401k_return = .02
                self.expected_401k_return = .02
            elif self.age >= self.retirement_age - 5:
                self.age += 1
                # close to retirement, time to invest money much more safely

                monthly_contribution, overage = self.check_contributions()

                monthly_outside_contribution = self.calculate_outside_investments(overage)

                total_outside_investments += monthly_outside_contribution * 12
                total_outside_investments += self.yearly_interest(total_outside_investments, self.expected_non401k_return)

                self.expected_non401k_return -= self.expected_non401k_return *.20
                self.expected_401k_return -= self.expected_401k_return * .20

            else:
                self.age += 1
                self.principal_401k += self.return_401k_contribution_yr()

                monthly_contribution, overage = self.check_contributions()

                monthly_outside_contribution = self.calculate_outside_investments(overage)

                total_outside_investments += monthly_outside_contribution * 12
                total_outside_investments += self.yearly_interest(total_outside_investments, self.expected_non401k_return)

            for num in range(12):
                if months[num] == "Jan":
                    total += monthly_contribution
                    total += total * (self.expected_401k_return / 12)
                    print(f"\nYear {i} - Month {months[num]}\n\tAmount Invested:\t{monthly_contribution}\n\tTotal Portfolio:\t{total}")
                elif months[num] == "Dec":
                    monthly_contribution += self.return_profit_share_yr()
                    total += monthly_contribution
                    total += total * (self.expected_401k_return / 12)
                    print(f"\nYear {i} - Month {months[num]}\n\tAmount Invested:\t{monthly_contribution}\n\tTotal 401k:\t\t{total}\n\tOutside Investments:\t{total_outside_investments}\n\tOI_Per_Month:\t\t{monthly_outside_contribution}\n\tYearly Salary:\t\t{self.salary}\n\tOverage:\t\t{overage}")
                else:
                    total += monthly_contribution
                    total += total * (self.expected_401k_return / 12)
            
            self.dollar_value_calc()
            self.salary_bump()
            if self.age >= self.retirement_age:
                total_outside_investments -= self.retirement_distrobution

        print(f"Value of dollar after {self.sim_years} years             \t\t: {round(self.dollar_value,2)}")
        print(f"Current Age:                                             \t\t: {self.age}")
        print(f"401k Portfolio value in Current_year dollars             \t\t: {round(total * self.dollar_value,2):,}")
        print(f"Non-401k Portfolio value in Current_year Dollars         \t\t: {round(total_outside_investments * self.dollar_value,2):,}")
        print(f"Principal Value of 401k                                  \t\t: {round(self.principal_401k,2):,}")
        print(f"Principal Value of Non-401k invesments                   \t\t: {round(self.principal_non401k,2):,}")
        print(f"Total value of 401k in Current_year + Sim_year dollars   \t\t: {round(total,2):,}")
        print(f"Total value of Non401k in Current_year + Sim_year dollars\t\t: {round(total_outside_investments,2):,}")



def main():
    luke = Investor(age=                            26,
                    starting_401k_principle=        10_000,
                    starting_non401k_principle=     0,
                    amnt_invst_401k_percentage=     .15,
                    amnt_invst_non401k=             500,
                    amnt_invst_non401k_increase=    .025,
                    salary=                         110_000,
                    salary_increase=                .035,
                    years_to_sim=                   40,
                    expected_401k_return=           .07,
                    expected_non401k_return=        .0984,
                    profit_share_percentage=        .03,
                    company_401k_investment_per=    .05,
                    retirement_age=                 65,
                    retirement_distrobution=        0)
    luke.invest()

if __name__ == '__main__':
    main()