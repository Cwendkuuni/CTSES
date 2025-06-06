package org.apache.commons.cli;

import org.junit.Test;
import static org.junit.Assert.*;
import java.util.Iterator;
import java.util.List;
import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.Option;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.junit.runner.RunWith;

@RunWith(EvoRunner.class) 
@EvoRunnerParameters(mockJVMNonDeterminism = true, useVFS = true, useVNET = true, resetStaticState = true, separateClassLoader = false) 
 public class CommandLine_ESTest extends CommandLine_ESTest_scaffolding {

    private static final String DEFAULT_OPTION_VALUE = "org.apache.commons.cli.CommandLine";
    private static final String DEFAULT_OPTION_DESCRIPTION = "D1,L";
    private static final String DEFAULT_OPTION_NAME = "";
    private static final String DEFAULT_OPTION_LONG_NAME = "\"Jd";
    private static final String DEFAULT_OPTION_ARG = " ";
    private static final String DEFAULT_OPTION_ARG_DESCRIPTION = "*,Od<*udS<o(OWc";
    private static final String DEFAULT_OPTION_ARG_VALUE = "NUK,JY";
    private static final String DEFAULT_OPTION_VALUE_IF_NULL = "26|#HQ,Xt";

    @Test(timeout = 4000)
    public void testGetOptionValuesWithEmptyString() throws Throwable {
        // Given: A new CommandLine instance
        CommandLine commandLine = new CommandLine();

        // When: Retrieving option values for an empty string
        String[] optionValues = commandLine.getOptionValues("");

        // Then: The option values should be null
        assertNull("Option values should be null for an empty string", optionValues);
    }

    @Test(timeout = 4000)
    public void testOptionHasNoOptionalArg() throws Throwable {
        // Given: A new CommandLine instance with an option
        CommandLine commandLine = new CommandLine();
        Option option = new Option(null, false, "*");
        commandLine.addOption(option);

        // Then: The option should not have an optional argument
        assertFalse("Option should not have an optional argument", option.hasOptionalArg());
    }

    @Test(timeout = 4000)
    public void testGetOptionValueWithDefault() throws Throwable {
        // Given: A new CommandLine instance with an option
        CommandLine commandLine = new CommandLine();
        Option option = new Option(DEFAULT_OPTION_NAME, DEFAULT_OPTION_LONG_NAME, true, DEFAULT_OPTION_DESCRIPTION);
        option.addValue(DEFAULT_OPTION_VALUE);
        commandLine.addOption(option);

        // When: Retrieving option value with a default
        String optionValue = commandLine.getOptionValue("--", null);

        // Then: The option value should be the default value
        assertNotNull("Option value should not be null", optionValue);
        assertEquals("Option value should match the default value", DEFAULT_OPTION_VALUE, optionValue);
    }

    @Test(timeout = 4000)
    public void testGetOptionValueForNonExistentOption() throws Throwable {
        // Given: A new CommandLine instance with an option
        CommandLine commandLine = new CommandLine();
        Option option = new Option(DEFAULT_OPTION_ARG, DEFAULT_OPTION_ARG, true, DEFAULT_OPTION_ARG_DESCRIPTION);
        commandLine.addOption(option);

        // When: Retrieving option value for a non-existent option
        String optionValue = commandLine.getOptionValue(DEFAULT_OPTION_ARG);

        // Then: The option value should be null
        assertNull("Option value should be null for a non-existent option", optionValue);
    }

    @Test(timeout = 4000)
    public void testGetOptionObjectWithEmptyString() throws Throwable {
        // Given: A new CommandLine instance with an option
        CommandLine commandLine = new CommandLine();
        Option option = new Option(DEFAULT_OPTION_NAME, DEFAULT_OPTION_LONG_NAME, true, DEFAULT_OPTION_DESCRIPTION);
        option.addValue(DEFAULT_OPTION_VALUE);
        commandLine.addOption(option);

        // When: Retrieving option object for an empty string
        Object optionObject = commandLine.getOptionObject("");

        // Then: The option object should be null
        assertNull("Option object should be null for an empty string", optionObject);
    }

    @Test(timeout = 4000)
    public void testGetOptionObjectForNonExistentOption() throws Throwable {
        // Given: A new CommandLine instance with an option
        CommandLine commandLine = new CommandLine();
        Option option = new Option(DEFAULT_OPTION_NAME, false, "");
        commandLine.addOption(option);

        // When: Retrieving option object for a non-existent option
        Object optionObject = commandLine.getOptionObject("");

        // Then: The option object should be null
        assertNull("Option object should be null for a non-existent option", optionObject);
    }

    @Test(timeout = 4000)
    public void testHasOptionWithEmptyString() throws Throwable {
        // Given: A new CommandLine instance with an option
        CommandLine commandLine = new CommandLine();
        Option option = new Option(DEFAULT_OPTION_NAME, false, "");
        commandLine.addOption(option);

        // When: Checking if the option exists
        boolean hasOption = commandLine.hasOption("");

        // Then: The option should exist
        assertTrue("Option should exist for an empty string", hasOption);
    }

    @Test(timeout = 4000)
    public void testAddArgument() throws Throwable {
        // Given: A new CommandLine instance
        CommandLine commandLine = new CommandLine();

        // When: Adding an argument
        commandLine.addArg(DEFAULT_OPTION_ARG_VALUE);

        // Then: No exception should be thrown
    }

    @Test(timeout = 4000)
    public void testGetArgsWithNoArguments() throws Throwable {
        // Given: A new CommandLine instance
        CommandLine commandLine = new CommandLine();

        // When: Retrieving arguments
        String[] args = commandLine.getArgs();

        // Then: The arguments array should be empty
        assertEquals("Arguments array should be empty", 0, args.length);
    }

    @Test(timeout = 4000)
    public void testGetOptionObjectForNonExistentCharOption() throws Throwable {
        // Given: A new CommandLine instance
        CommandLine commandLine = new CommandLine();

        // When: Retrieving option object for a non-existent char option
        Object optionObject = commandLine.getOptionObject('z');

        // Then: The option object should be null
        assertNull("Option object should be null for a non-existent char option", optionObject);
    }

    @Test(timeout = 4000)
    public void testGetArgListWithNoArguments() throws Throwable {
        // Given: A new CommandLine instance
        CommandLine commandLine = new CommandLine();

        // When: Retrieving argument list
        List<?> argList = commandLine.getArgList();

        // Then: The argument list should be empty
        assertTrue("Argument list should be empty", argList.isEmpty());
    }

    @Test(timeout = 4000)
    public void testGetOptionValueWithDefaultForNonExistentCharOption() throws Throwable {
        // Given: A new CommandLine instance
        CommandLine commandLine = new CommandLine();

        // When: Retrieving option value with a default for a non-existent char option
        String optionValue = commandLine.getOptionValue('p', DEFAULT_OPTION_VALUE_IF_NULL);

        // Then: The option value should be the default value
        assertNotNull("Option value should not be null", optionValue);
        assertEquals("Option value should match the default value", DEFAULT_OPTION_VALUE_IF_NULL, optionValue);
    }

    @Test(timeout = 4000)
    public void testGetOptionValueForNonExistentCharOption() throws Throwable {
        // Given: A new CommandLine instance
        CommandLine commandLine = new CommandLine();

        // When: Retrieving option value for a non-existent char option
        String optionValue = commandLine.getOptionValue('=');

        // Then: The option value should be null
        assertNull("Option value should be null for a non-existent char option", optionValue);
    }

    @Test(timeout = 4000)
    public void testGetOptionValuesForNonExistentCharOption() throws Throwable {
        // Given: A new CommandLine instance
        CommandLine commandLine = new CommandLine();

        // When: Retrieving option values for a non-existent char option
        String[] optionValues = commandLine.getOptionValues('d');

        // Then: The option values should be null
        assertNull("Option values should be null for a non-existent char option", optionValues);
    }

    @Test(timeout = 4000)
    public void testIteratorNotNull() throws Throwable {
        // Given: A new CommandLine instance
        CommandLine commandLine = new CommandLine();

        // When: Retrieving the iterator
        Iterator<?> iterator = commandLine.iterator();

        // Then: The iterator should not be null
        assertNotNull("Iterator should not be null", iterator);
    }

    @Test(timeout = 4000)
    public void testGetOptionsWithNoOptions() throws Throwable {
        // Given: A new CommandLine instance
        CommandLine commandLine = new CommandLine();

        // When: Retrieving options
        Option[] options = commandLine.getOptions();

        // Then: The options array should be empty
        assertEquals("Options array should be empty", 0, options.length);
    }

    @Test(timeout = 4000)
    public void testHasOptionForNonExistentCharOption() throws Throwable {
        // Given: A new CommandLine instance
        CommandLine commandLine = new CommandLine();

        // When: Checking if a non-existent char option exists
        boolean hasOption = commandLine.hasOption('E');

        // Then: The option should not exist
        assertFalse("Option should not exist for a non-existent char option", hasOption);
    }
}