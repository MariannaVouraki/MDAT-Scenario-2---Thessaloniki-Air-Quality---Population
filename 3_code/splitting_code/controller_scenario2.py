from step1_LoadEnvironmentalData import run_step_1
from step2_AggregateAndComputeMeanPollutantLevels import run_step_2
from step3_LoadDemographicData import run_step_3
from step4_CleanAndNormaliseDemographics import run_step_4
from step5_MergeAndComputePerCapita import run_step_5
from step6_AssessComplianceWithEULimits import run_step_6
from step7_GenerateGraphsAndVisualSummaries import run_step_7

def main():
    step1 = run_step_1()
    step2 = run_step_2(step1)
    step3 = run_step_3()
    step4 = run_step_4(step3)
    step5 = run_step_5(step2, step4)
    step6 = run_step_6(step5)
    run_step_7(step6)

if __name__ == "__main__":
    main()
