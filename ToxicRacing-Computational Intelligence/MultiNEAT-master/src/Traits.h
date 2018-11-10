//
// Created by peter on 28.04.17.
//

#ifndef MULTINEAT_TRAITS_H
#define MULTINEAT_TRAITS_H

#include <string>
#include <boost/any.hpp>
#include <boost/variant.hpp>
#include <cmath>

namespace bs = boost;

namespace NEAT
{
    typedef bs::variant<int, bool, double, std::string> TraitType;

    class IntTraitParameters
    {
    public:
        int min, max;
        int mut_power; // magnitude of max change up/down
        double mut_replace_prob; // probability to replace when mutating

        IntTraitParameters()
        {
            min = 0; max = 0;
            mut_replace_prob = 0;
        }
    };
    class FloatTraitParameters
    {
    public:
        double min, max;
        double mut_power; // magnitude of max change up/down
        double mut_replace_prob; // probability to replace when mutating

        FloatTraitParameters()
        {
            min = 0; max = 0;
            mut_replace_prob = 0;
        }
    };
    class StringTraitParameters
    {
    public:
        std::vector<std::string> set; // the set of possible strings
        std::vector<double> probs; // their respective probabilities for appearance
    };

    class TraitParameters
    {
    public:
        double m_ImportanceCoeff;
        double m_MutationProb;

        std::string type; // can be "int", "bool", "float", "string"
        bs::variant<IntTraitParameters, FloatTraitParameters, StringTraitParameters> m_Details;

        std::string dep_key; // counts only if this other trait exists..
        std::vector<TraitType> dep_values; // and has one of these values

        // keep dep_key empty and no conditional logic will apply

        TraitParameters()
        {
            m_ImportanceCoeff = 0;
            m_MutationProb = 0;
            type = "int";
            m_Details = IntTraitParameters();
            dep_key = "";
            dep_values.push_back( std::string("") );
        }
    };

    class Trait
    {
    public:
        TraitType value;

        Trait()
        {
            value = 0;
            dep_values.push_back(0);
            dep_key = "";
        }

        std::string dep_key; // counts only if this other trait exists..
        std::vector<TraitType> dep_values; // and has this value
    };

}
#endif //MULTINEAT_TRAITS_H
