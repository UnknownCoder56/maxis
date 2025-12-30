"""
Modal submission handlers
"""

import discord
from bot.helper import get_random_color, credit_balance, debit_balance

PRIZE_OR_COST = 9000


def _get_main():
    """Lazy import Main to avoid circular imports with bot.main."""
    from bot.main import Main  # type: ignore

    return Main


class ModalsListener:
    @staticmethod
    async def on_modal_submit(interaction: discord.Interaction):
        """Handle modal submissions"""
        custom_id = interaction.data.get("custom_id", "") if interaction.data else None
        if not custom_id:
            Main = _get_main()
            if await debit_balance(
                PRIZE_OR_COST,
                interaction,
                Main.CONNSTR,
                Main.user_settings_map,
                Main.balance_map,
            ):
                embed = discord.Embed(
                    title="Failure!",
                    description=f"Hacking failed due to wrong answer. You lost :coin: {PRIZE_OR_COST}",
                    color=get_random_color(),
                )
                await interaction.response.send_message(embed=embed)
            return

        if custom_id.startswith("laptop_code_result"):
            await ModalsListener._handle_laptop_code(interaction, custom_id)

    @staticmethod
    async def _handle_laptop_code(interaction: discord.Interaction, custom_id: str):
        """Handle laptop code submission"""
        try:
            Main = _get_main()
            parts = custom_id.split("_")
            if len(parts) < 4:
                return

            correct_answer = int(parts[3])
            answer_input = (
                interaction.data.get("components", [{}])[0].get("components", [{}])[0]
                if interaction.data
                else None
            )

            if not answer_input:
                if await debit_balance(
                    PRIZE_OR_COST,
                    interaction,
                    Main.CONNSTR,
                    Main.user_settings_map,
                    Main.balance_map,
                ):
                    embed = discord.Embed(
                        title="Failure!",
                        description=f"Hacking failed due to wrong answer. You lost :coin: {PRIZE_OR_COST}",
                        color=get_random_color(),
                    )
                    await interaction.response.send_message(embed=embed)
                return

            user_input = answer_input.get("value", "")

            try:
                answer = int(user_input)
                if answer == correct_answer:
                    if await credit_balance(
                        PRIZE_OR_COST,
                        interaction,
                        Main.CONNSTR,
                        Main.user_settings_map,
                        Main.balance_map,
                    ):
                        embed = discord.Embed(
                            title="Success!",
                            description=f"Hacking successful! You got :coin: {PRIZE_OR_COST}",
                            color=get_random_color(),
                        )
                        await interaction.response.send_message(embed=embed)
                else:
                    if await debit_balance(
                        PRIZE_OR_COST,
                        interaction,
                        Main.CONNSTR,
                        Main.user_settings_map,
                        Main.balance_map,
                    ):
                        embed = discord.Embed(
                            title="Failure!",
                            description=f"Hacking failed due to wrong answer. You lost :coin: {PRIZE_OR_COST}",
                            color=get_random_color(),
                        )
                        await interaction.response.send_message(embed=embed)
            except ValueError:
                if await debit_balance(
                    PRIZE_OR_COST,
                    interaction,
                    Main.CONNSTR,
                    Main.user_settings_map,
                    Main.balance_map,
                ):
                    embed = discord.Embed(
                        title="Failure!",
                        description=f"Hacking failed due to incorrect input type. You lost :coin: {PRIZE_OR_COST}",
                        color=get_random_color(),
                    )
                    await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(f"Error handling laptop code: {e}")
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="An error occurred processing your answer.",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
