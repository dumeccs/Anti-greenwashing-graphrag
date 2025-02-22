test_data = [
    {
        "question": "What are the indications of greenwashing in this statement? 'Our new product is 100% natural and completely harmless to the environment, making it the best choice for eco-conscious consumers.' Rephrase the statement to avoid greenwashing.",
        "ground_truth": "The indications of greenwashing in this statement include the use of absolute terms like '100% natural' and 'completely harmless,' which are difficult to substantiate and may exaggerate the product's environmental benefits. A more reasonable claim could be: 'Our new product is made from natural ingredients and is designed to minimize environmental impact, making it a good choice for eco-conscious consumers.'",
        "contexts": [
            "The FCA’s anti-greenwashing rule requires that sustainability claims must be fair, clear, and not misleading. Claims should avoid absolute terms like '100%' unless they can be fully substantiated.",
            "The CMA’s Green Claims Code emphasizes that environmental claims should be truthful, accurate, and not exaggerated. Firms should avoid making claims that cannot be supported by robust evidence."
        ]
    },
    {
        "question": "What are the indications of greenwashing in this claim? 'Our packaging is now 100% biodegradable, helping to save the planet one package at a time.' Rephrase the claim to make it more reasonable and non-greenwashing.",
        "ground_truth": "The indications of greenwashing in this claim include the use of '100% biodegradable' without specifying the conditions required for biodegradation and the exaggerated claim of 'saving the planet.' A more reasonable claim could be: 'Our packaging is designed to be biodegradable under specific conditions, contributing to reducing waste and environmental impact.'",
        "contexts": [
            "The FCA’s anti-greenwashing rule requires that claims about biodegradability must be clear and specify the conditions under which the product will biodegrade.",
            "The CMA’s Green Claims Code states that environmental claims should not exaggerate the benefits of a product and should provide clear and accurate information."
        ]
    },
    {
        "question": "What are the indications of greenwashing in this advertisement? 'Our energy-efficient appliances reduce your carbon footprint to zero, making your home completely eco-friendly.' Rephrase the advertisement to avoid greenwashing.",
        "ground_truth": "The indications of greenwashing in this advertisement include the claim of reducing the carbon footprint to 'zero,' which is likely exaggerated and difficult to substantiate. A more reasonable claim could be: 'Our energy-efficient appliances are designed to significantly reduce your carbon footprint, helping you create a more eco-friendly home.'",
        "contexts": [
            "The FCA’s anti-greenwashing rule requires that claims about carbon footprint reduction must be accurate and supported by evidence. Exaggerated claims like 'zero carbon footprint' are considered misleading.",
            "The CMA’s Green Claims Code emphasizes that claims should be truthful and not exaggerate the environmental benefits of a product."
        ]
    },
    {
        "question": "What are the indications of greenwashing in this statement? 'Our company is proud to be carbon neutral, with all our operations having no impact on the environment.' Rephrase the statement to make it more reasonable and non-greenwashing.",
        "ground_truth": "The indications of greenwashing in this statement include the claim of being 'carbon neutral' without providing evidence or details about how this was achieved, and the assertion of having 'no impact on the environment,' which is likely exaggerated. A more reasonable claim could be: 'Our company is committed to reducing our carbon footprint and has taken significant steps to offset our emissions, striving to minimize our environmental impact.'",
        "contexts": [
            "The FCA’s anti-greenwashing rule requires that claims about carbon neutrality must be substantiated with evidence and should not exaggerate the environmental impact of a company’s operations.",
            "The CMA’s Green Claims Code states that claims about carbon neutrality should be clear, accurate, and supported by credible evidence."
        ]
    },
    {
        "question": "What are the indications of greenwashing in this claim? 'Our new clothing line is made from 100% sustainable materials, ensuring a completely eco-friendly fashion choice.' Rephrase the claim to avoid greenwashing.",
        "ground_truth": "The indications of greenwashing in this claim include the use of '100% sustainable materials' without specifying what makes the materials sustainable and the assertion of being 'completely eco-friendly,' which is difficult to substantiate. A more reasonable claim could be: 'Our new clothing line is made from materials that prioritize sustainability, such as organic cotton and recycled fabrics, offering a more eco-friendly fashion choice.'",
        "contexts": [
            "The FCA’s anti-greenwashing rule requires that claims about sustainability must be clear, accurate, and supported by evidence. Vague terms like '100% sustainable' are considered misleading.",
            "The CMA’s Green Claims Code emphasizes that claims about sustainability should be specific and provide clear information about the environmental benefits of the product."
        ]
    },
    {
        "question": "What are the indications of greenwashing in this statement? 'Our electric vehicles are the greenest option on the market, with zero emissions and no environmental impact.' Rephrase the statement to make it more reasonable and non-greenwashing.",
        "ground_truth": "The indications of greenwashing in this statement include the claim of being the 'greenest option on the market' without providing evidence, and the assertion of 'zero emissions and no environmental impact,' which ignores the environmental impact of manufacturing and battery disposal. A more reasonable claim could be: 'Our electric vehicles produce zero tailpipe emissions and are designed to minimize environmental impact, making them a greener choice for transportation.'",
        "contexts": [
            "The FCA’s anti-greenwashing rule requires that claims about environmental impact must be accurate and consider the full life cycle of the product. Exaggerated claims like 'no environmental impact' are considered misleading.",
            "The CMA’s Green Claims Code states that claims should be truthful and not exaggerate the environmental benefits of a product."
        ]
    },
    {
        "question": "What are the indications of greenwashing in this claim? 'Our cleaning products are 100% chemical-free and completely safe for the environment.' Rephrase the claim to avoid greenwashing.",
        "ground_truth": "The indications of greenwashing in this claim include the use of '100% chemical-free,' which is scientifically inaccurate, and the assertion of being 'completely safe for the environment,' which is difficult to substantiate. A more reasonable claim could be: 'Our cleaning products are made with natural ingredients and are designed to be safer for the environment compared to traditional cleaning products.'",
        "contexts": [
            "The FCA’s anti-greenwashing rule requires that claims about product safety and environmental impact must be accurate and supported by evidence. Claims like '100% chemical-free' are considered misleading.",
            "The CMA’s Green Claims Code emphasizes that claims should be truthful and not exaggerate the environmental benefits of a product."
        ]
    },
    {
        "question": "What are the indications of greenwashing in this statement? 'Our company has achieved 100% renewable energy usage, making us a leader in sustainability.' Rephrase the statement to make it more reasonable and non-greenwashing.",
        "ground_truth": "The indications of greenwashing in this statement include the claim of '100% renewable energy usage' without providing evidence or details about how this was achieved, and the assertion of being a 'leader in sustainability,' which is subjective. A more reasonable claim could be: 'Our company has made significant progress in transitioning to renewable energy sources, and we are committed to further reducing our environmental impact.'",
        "contexts": [
            "The FCA’s anti-greenwashing rule requires that claims about renewable energy usage must be substantiated with evidence and should not exaggerate the company’s sustainability achievements.",
            "The CMA’s Green Claims Code states that claims about sustainability leadership should be supported by credible evidence and should not be exaggerated."
        ]
    }
]