"""Config flow for Context Provider integration."""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback, HomeAssistant
from homeassistant.data_entry_flow import FlowResult
import logging

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class ContextProviderConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Context Provider."""

    VERSION = 1

    @classmethod
    def is_matching(cls, domain: str) -> bool:
        """Check if the domain matches this config flow.

        Args:
            domain (str): The domain to check.

        Returns:
            bool: True if the domain matches, False otherwise.

        """
        return domain == DOMAIN

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Handle the user step of the config flow.

        This step is triggered when the user initiates the configuration flow.

        Args:
            user_input (dict | None): The user input provided during the step.

        Returns:
            FlowResult: The result of the config flow step.

        """
        if user_input is not None:
            # Create a ConfigEntry with the provided user input
            return self.async_create_entry(title="Context Provider", data=user_input)

        # Show the form if no user input is provided
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required("test_option", default="default"): str}
            ),
        )

    async def async_step_options(self, user_input: dict | None = None) -> FlowResult:
        """Handle the options step of the config flow.

        This step is triggered when the user accesses the options for the integration.

        Args:
            user_input (dict | None): The user input provided during the step.

        Returns:
            FlowResult: The result of the options flow step.
        """
        _LOGGER.debug("async_step_options called with user_input: %s", user_input)
        if user_input is not None:
            # Update the options with the provided user input
            return self.async_create_entry(title="", data=user_input)

        # Show the form if no user input is provided
        return self.async_show_form(
            step_id="options",
            data_schema=vol.Schema(
                {vol.Required("option_key", default="default_value"): str}
            ),
        )

    async def async_update_entry(
        self, hass: HomeAssistant, entry: config_entries.ConfigEntry
    ) -> None:
        """Update the configuration entry.

        This method is called when the user updates the configuration of the integration.

        Args:
            hass (HomeAssistant): The Home Assistant instance.
            entry (ConfigEntry): The configuration entry to update.
        """
        # Update the configuration entry with new data
        hass.config_entries.async_update_entry(entry, data=entry.data)

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Return the options flow handler for this config entry."""
        return ContextProviderOptionsFlowHandler(config_entry)


@callback
def async_get_options_flow(
    config_entry: config_entries.ConfigEntry,
) -> "ContextProviderOptionsFlowHandler":
    """Get the options flow handler for the config entry.

    Args:
        config_entry (ConfigEntry): The configuration entry for the integration.

    Returns:
        ContextProviderOptionsFlowHandler: The options flow handler instance.
    """
    _LOGGER.debug("async_get_options_flow called for config entry: %s", config_entry)
    return ContextProviderOptionsFlowHandler(config_entry)


class ContextProviderOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle the options flow for Context Provider."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize the options flow handler."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict | None = None) -> FlowResult:
        """Handle the initial step of the options flow.

        This step is triggered when the user accesses the options for the integration.

        Args:
            user_input (dict | None): The user input provided during the step.

        Returns:
            FlowResult: The result of the options flow step.
        """
        if user_input is not None:
            # Update the config entry with the new options
            self.hass.config_entries.async_update_entry(
                self.config_entry, options=user_input
            )
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "option_key",
                        default=self.config_entry.options.get(
                            "option_key", "default_value"
                        ),
                    ): str
                }
            ),
        )
