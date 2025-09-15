# AI Agents vs Traditional Apps: A Simple Comparison
    Using a beach-town weather utility as an example

Living in San Diego, I enjoy learning to surf. Looking for perfect weather conditions before heading to the beach, I used to check weather on my phone and also find out the water temperature online.

Then I decided to write a Python App to do those for me, and inform me if both the air and water temperatures are above my personal thresholds (76°F and 69°F).

**Gemini CLI** wrote a Python method, which relies on **SerpApi** for retrieving and extracting the weather forecast, but it did not work. To achieve those tasks, the code depends on specific **keys** in the retrieved data (Python dict or JSON). To debug, I outputted the data into a JSON file, and scrolled down the huge file. Turns out that the key-structure is complex and different from those assumed by Gemini CLI.

With detailed key info, I was able to get the code to work. Working out all the details, I finally extracted the forecast.

After a few days, the code stopped working. The data I pored over had Celsius and PM, as examples, while the new data had Fahrenheit and p.m.! Simply speaking, the data is dynamic!

At this point, I decided to give AI agents a try. My weather AI agent is posted on [Github](https://github.com/qiangliu-sd/ai-agent-LangGraph).

Basically, I defined two Google searches via SerpApi as *tools* (i.e., Py-methods) and handed them to **Gemini 2.5 Flash** (the LLM I used, or the *brain* of my agent). By definition, **a LLM with tools are called an AI agent**.

After I gave it the prompt, Gemini handled all the tool calls and the details of information extraction, without any of my coding!

I tested four prompts progressively. The agent worked very well for me. The prompts and truncated replies are list below:
1. *weather forecast Poway, California* ([click to see the reply](texts/weather_forecast.txt))
2. *weather forecast, water temperature, Solana Beach California* ([click to see the reply](texts/weather_forecast_water.txt))
3. *hourly weather forecast, water temperature, Solana Beach California* ([click to see the reply](texts/hourly_forecast_water.txt))
4. *3 PM weather forecast, water temperature, Solana Beach California* ([click to see the reply](texts/3PM_forecast_water.txt))
