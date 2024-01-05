SELECT * FROM coviddeaths;
SELECT * FROM covidvaccinatiion;

-- Select data that we are going to use 
-- Using Covid Deaths table
SELECT 
LOCATION, date, total_cases, new_cases, total_deaths, population 
FROM coviddeaths 
WHERE continent is NOT NULL
ORDER BY 1, 2;

-- Looking at total cases vs total deaths in Pakistan, you can chan the country according to your REQUIREMENT in '%_______%'
SELECT 
LOCATION, date, total_cases, total_deaths, (total_deaths/total_cases)*100 as Total_Deaths_Percentage
FROM coviddeaths 
WHERE location like '%pakistan%' AND continent is NOT NULL
ORDER BY Total_Deaths_Percentage DESC;

-- Looking at total cases vs population
-- Show that what percentage of population got effected by covid

SELECT 
location, date, total_cases, population, (total_cases/population)*100 as Population_effected
FROM coviddeaths
WHERE location like '%pakistan%' AND continent is NOT NULL
ORDER BY Population_effected DESC;

-- Looking at countries with highest infection rate compared to population 
SELECT 
location,  MAX(total_cases) as Highest_count, population, MAX((total_cases/population))*100 as Percent_Population_effected
FROM coviddeaths
WHERE continent is NOT NULL
GROUP BY location, population
ORDER BY Percent_Population_effected DESC;

-- Showing Countries with highest Death COUNT per population
SELECT 
location, MAX(total_deaths) as Total_Death_Count
FROM coviddeaths
WHERE continent is NOT NULL
GROUP BY location
ORDER BY Total_Death_Count DESC;

-- Let'd Break things down by continent
-- Showing continent with the highest death count per population
SELECT 
continent, MAX(total_deaths) as Total_Death_Count
FROM coviddeaths
WHERE continent is NOT NULL
GROUP BY continent
ORDER BY Total_Death_Count DESC;    

-- Global NUMBER
SELECT SUM(new_cases) as Total_Cases, SUM(new_deaths) as Total_Deaths , ((SUM(new_deaths)/SUM(new_cases))*100) as Death_Percentage
FROM coviddeaths
WHERE continent IS NOT NULL
ORDER BY Death_Percentage;


-- Joining Both TABLE
-- Looking at Total Population vs Vaccination
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(vac.new_vaccinations) OVER (Partition by dea.Location Order by dea.location, dea.Date) as RollingPeopleVaccinated
From coviddeaths dea
Join covidvaccinatiion vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null 


-- Using CTE to perform Calculation on Partition By in previous query
With PopvsVac (Continent, Location, Date, Population, New_Vaccinations, RollingPeopleVaccinated)
as
(
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(vac.new_vaccinations) OVER (Partition by dea.Location Order by dea.location, dea.Date) as RollingPeopleVaccinated
From coviddeaths dea
Join covidvaccinatiion vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null 
)
Select *, (RollingPeopleVaccinated/Population)*100
From PopvsVac


-- Using Temp Table to perform Calculation on Partition By in previous query
DROP Table if exists PercentPopulationVaccinated

Create Table PercentPopulationVaccinated
(
Continent VARCHAR(255),
Location VARCHAR(255),
Date VARCHAR(255),
Population BIGINT,
New_vaccinations INT,
RollingPeopleVaccinated INT
)

INSERT INTO PercentPopulationVaccinated
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(vac.new_vaccinations) OVER (Partition by dea.Location Order by dea.location, dea.Date) as RollingPeopleVaccinated
From coviddeaths dea
Join covidvaccinatiion vac
	On dea.location = vac.location
	and dea.date = vac.date

SELECT *, (RollingPeopleVaccinated/Population)*100 FROM PercentPopulationVaccinated;

-- Creating View to store data for later visualizations
Create View PercentagePopulationVaccinated as
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(vac.new_vaccinations) OVER (Partition by dea.Location Order by dea.location, dea.Date) as RollingPeopleVaccinated
From coviddeaths dea
Join covidvaccinatiion vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null;

SELECT * FROM PercentagePopulationVaccinated;