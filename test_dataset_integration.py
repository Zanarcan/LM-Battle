#!/usr/bin/env python3
"""
Test script to demonstrate dataset integration in the attacker module
"""

from src.attacker import AdvancedAttacker, AttackStrategy

def test_dataset_attacks():
    """Test the dataset-based attack generation"""

    print("🧪 Testing Dataset Integration in ART Project")
    print("=" * 50)

    # Initialize attacker (this will also initialize datasets)
    attacker = AdvancedAttacker()

    print("\n📊 Testing different attack strategies:")
    print("-" * 40)

    strategies = [
        AttackStrategy.DIRECT,
        AttackStrategy.PARAPHRASE,
        AttackStrategy.DATASET,  # This should use dataset prompts
        AttackStrategy.CONTEXT_BUILDING
    ]

    threats = ["CAE", "FSA", "MME"]

    for strategy in strategies:
        print(f"\n🎯 Strategy: {strategy.value.upper()}")
        for threat in threats:
            attack = attacker.generate_attack(strategy, threat)
            print(f"  {threat}: '{attack.content[:60]}...' (subtlety: {attack.subtlety})")

    print("\n✅ Dataset integration test completed!")
    print("\n💡 Note: The DATASET strategy uses prompts from:")
    print("   1. Pliny_HackAPrompt_Dataset (if authenticated)")
    print("   2. Local sample_adversarial_prompts.json (fallback)")

if __name__ == "__main__":
    test_dataset_attacks()
